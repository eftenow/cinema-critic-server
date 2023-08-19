from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from cinema_critic_server.common.models import Genre
from cinema_critic_server.content.models import Movie, Series
from cinema_critic_server.reviews.models import Review

UserModel = get_user_model()


class ContentModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Action")
        self.user = UserModel.objects.create_user(username='testuser', password='tester_pass', email='tester@abv.bg')

        self.movie = Movie.objects.create(
            name="test movie",
            year=2000,
            director="Martin Scorsese",
            stars="Al Pacino, Marlon Brando",
            trailer="https://www.youtube.com/embed/UaVTIH8mujA",
            image="https://www.shutterstock.com/shutterstock/photos/2276341383/display_1500/stock-vector-the-godfather-icon-symbol-text-design-vector-2276341383.jpg",
            length="2 hours 22 minutes",
            description="A test movie.",
            creator=self.user
        )
        self.movie.genres.add(self.genre)

        self.series = Series.objects.create(
            name="test series",
            year=1999,
            director="Martin Scorsese",
            stars="Al Pacino, Marlon Brando",
            trailer="https://www.youtube.com/embed/UaVTIH8mujA",
            image="https://www.shutterstock.com/shutterstock/photos/2276341383/display_1500/stock-vector-the-godfather-icon-symbol-text-design-vector-2276341383.jpg",
            length="40 minutes",
            description="A test series.",
            creator=self.user,
            seasons=2,
            episodes=20
        )
        self.series.genres.add(self.genre)

    def test_movie_creation(self):
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(self.movie.name, "test movie")

    def test_series_creation(self):
        self.assertEqual(Series.objects.count(), 1)
        self.assertEqual(self.series.name, "test series")

    def test_update_rating(self):
        content_type_movie = ContentType.objects.get_for_model(Movie)
        content_type_series = ContentType.objects.get_for_model(Series)

        Review.objects.create(user=self.user, content="great movie", rating=8, content_type=content_type_movie,
                              object_id=self.movie.id)
        Review.objects.create(user=self.user, content="trash movie", rating=1, content_type=content_type_movie,
                              object_id=self.movie.id)
        self.movie.update_rating()

        Review.objects.create(user=self.user, content="great series", rating=9, content_type=content_type_series,
                              object_id=self.series.id)
        self.series.update_rating()

        self.assertEqual(self.movie.rating, Decimal('4.50'))
        self.assertEqual(self.series.rating, Decimal('9'))

    def test_update_visits_count(self):
        initial_movie_visits = self.movie.visits
        initial_series_visits = self.series.visits

        self.movie.update_visits_count()
        self.series.update_visits_count()

        self.assertEqual(self.movie.visits, initial_movie_visits + 1)
        self.assertEqual(self.series.visits, initial_series_visits + 1)


class ContentViewListTest(ContentModelTest):
    def test_content_view_list(self):
        client = APIClient()
        url = reverse('content_list')
        response = client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)


class EditMovieTest(ContentModelTest):
    def test_edit_movie(self):
        client = APIClient()
        client.force_authenticate(self.user)

        url = reverse('movie_detail', args=[self.movie.id])

        new_data = {
            "name": "edited movie name",
        }
        response = client.patch(url, new_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.name, "edited movie name")


class EditSeriesTest(ContentModelTest):
    def test_edit_series(self):
        client = APIClient()
        client.force_authenticate(self.user)

        url = reverse('series_detail', args=[self.series.id])

        new_data = {
            "name": "edited series name",
        }
        response = client.patch(url, new_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.series.refresh_from_db()
        self.assertEqual(self.series.name, "edited series name")


class DeleteMovieTest(ContentModelTest):
    def test_delete_movie(self):
        client = APIClient()
        client.force_authenticate(self.user)

        url = reverse('movie_detail', args=[self.movie.id])

        response = client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Movie.objects.count(), 0)


class DeleteSeriesTest(ContentModelTest):
    def test_delete_series(self):
        client = APIClient()
        client.force_authenticate(self.user)

        url = reverse('series_detail', args=[self.series.id])

        response = client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Series.objects.count(), 0)
