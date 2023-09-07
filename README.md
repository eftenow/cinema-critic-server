<hr>
<h1>Cinema Critic Server</h1>
<p>
  This is the backend of the Cinema Critic project. The backend is a RESTful API built with Django REST API. The frontend, built on vanilla JavaScript, interacts with this backend to provide a complete user experience.
  You can find the front-end repository <a href='https://github.com/eftenow/cinema-critic-project' target='_blank' rel='noopener noreferrer'>here</a>.</p>
</p>
<hr>

<h2>Features</h2>
<p>The backend handles the logic for several models:</p>
<ul>
  <li>AppUser: Our custom user model.</li>
  <li>Profile: Extends the AppUser model to provide detailed user profiles.</li>
  <li>Movies and Series: Handles the details and categorization of various movies and series.</li>
  <li>Reviews: Allows users to leave reviews on movies and series.</li>
  <li>Genres: Classifies movies and series into various genres.</li>
</ul>
<p>Additional features include:</p>
<ul>
  <li>Pagination: Helps in handling large amounts of data by splitting it into pages.</li>
  <li>Filtration: Provides the ability to filter the content based on different parameters.</li>
  <li>Sorting: Allows the ordering of content based on specific fields.</li>
  <li>JWT Token Authorization: Provides secure user authentication through JWT tokens passed as cookies.</li>
</ul>
<hr>

<h2>Technologies Used</h2>
<p>The Cinema Critic Server is built with:</p>
<ul>
  <li>Django REST API: Our framework for building the API.</li>
  <li>Django ORM: Used for interacting with the database.</li>
  <li>JWT: For secure user authentication.</li>
</ul>
<hr>
<h2>Setup and Installation</h2>
<p>To set up and run this project locally, follow these steps:</p>
<ol>
  <li>Clone the repository: <code>git clone https://github.com/your-username/your-repo-url.git</code></li>
  <li>Get to the project directory</li>
  <li>Install the requirements: <code>pip install -r requirements.txt</code></li>
  <li>Run the migrations: <code>python manage.py migrate</code></li>
  <li>Start the server: <code>python manage.py runserver</code></li>
</ol>
<hr>
<h2>Usage</h2>
<p>Here's an example request for this API:</p>
<pre><code>
Example request: ../content/movies/1/  (GET)

Response:
{
    "id": 1,
    "name": "Test movie",
    "year": 2000,
    "rating": "4.93",
    "director": "Test Director",
    "stars": ["Marlon Brando", "Al Pacino"],
    "visits": 5,
    "genres": [
        "Action",
        "Drama"
    ],
    "trailer": "https://youtu.be/7qUw0UHREtg",
    "image": "https://img.freepik.com/premium-photo/image-colorful-galaxy-sky-generative-ai_791316-9864.jpg?w=2000",
    "length": "2 hours and 30 minutes",
    "created_at": "2023-07-22T07:59:15.866030Z",
    "slug": "test-movie-1",
    "description": "test description"
}
</code></pre>
<hr>
