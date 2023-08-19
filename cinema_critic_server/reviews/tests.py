from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


from cinema_critic_server.reviews.models import Review

UserModel = get_user_model()


class ReviewModelTestCase(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create_user(username='tester', password='tester_pass', email='tester@abv.bg')
        self.content_type = ContentType.objects.get_for_model(Review)

    def test_create_review(self):
        review = Review.objects.create(
            review_title="best movie ever",
            user=self.user,
            content="i like it a lot...",
            rating=10,
            content_type=self.content_type,
            object_id=1
        )
        self.assertEqual(review.review_title, "best movie ever")
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 10)


class ReviewViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(username='tester', password='tester_pass', email='tester@abv.bg')
        self.client.force_authenticate(user=self.user)
        self.content_type = ContentType.objects.get_for_model(Review)

        self.review = Review.objects.create(
            review_title="best movie ever",
            user=self.user,
            content="i like it a lot...",
            rating=10,
            content_type=self.content_type,
            object_id=1
        )

    def test_list_create_review(self):
        url = reverse('review_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_review_list(self):
        url = reverse('user_review_list', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
