# from django.test import RequestFactory, TestCase

# from ..views import get_movies
# from .mock_data import test_movies_resp


# class TestMovieView(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()
#         self.movies = test_movies_resp

#     def test_details(self):
#         # Create an instance of a GET request.
#         request = self.factory.get('/movies')

#         # Test get_movies() as if it were deployed at /movies
#         response = get_movies(request)
#         self.assertEqual(response.status_code, 200)
