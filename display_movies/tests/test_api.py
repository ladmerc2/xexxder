import unittest
import requests_mock

from django.test import RequestFactory
from unittest.mock import MagicMock, patch
from ..services import api
from ..views import get_movies
from .mock_data import test_movie_url, test_movie_resp, test_people_url, test_people_resp, test_movies_resp, test_movie_url_second


class TestGetMovie(unittest.TestCase):

    MOCK_ADDRESS = f'{test_movie_url}?fields=id,title,name,description,release_date'

    @requests_mock.Mocker()
    def test_movie(self, m):

        m.get(self.MOCK_ADDRESS,
              json=test_movie_resp)
        req = api.get_movies(test_movie_url)

        self.assertEqual(len(req), len(test_movie_resp))
        self.assertEqual(req['title'], "Castle in the Sky")

    @requests_mock.Mocker()
    def test_movie_bad_request(self, m):

        m.get(self.MOCK_ADDRESS,
              json=test_movie_resp, status_code=400)
        req = api.get_movies(test_movie_url)

        self.assertEqual(req, None)


class TestGetPeople(unittest.TestCase):

    MOCK_ADDRESS = test_people_url

    @requests_mock.Mocker()
    def test_people(self, m):

        m.get(self.MOCK_ADDRESS,
              json=test_people_resp)
        req = api.get_people()

        self.assertEqual(len(req), len(test_people_resp))
        self.assertEqual(req[0]['name'], "Ashitaka")

    @requests_mock.Mocker()
    def test_people_bad_request(self, m):

        m.get(self.MOCK_ADDRESS,
              json=test_people_resp, status_code=400)
        req = api.get_people()

        self.assertEqual(req, None)


data = {}
expire = 60


class TestMappingLogic(unittest.TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.movies = test_movies_resp

    def set(key, val):
        data[key] = val

    def get(self, key, value):
        return data[key]

    def expire(self, value):
        return expire

    def delete(self, key, value):
        data[key] = None

    MOCK_PEOPLE_ADDRESS = test_people_url
    MOCK_MOVIE_ADDRESS_ONE = f'{test_movie_url}?fields=id,title,name,description,release_date'
    MOCK_MOVIE_ADDRESS_TWO = f'{test_movie_url_second}?fields=id,title,name,description,release_date'

    @requests_mock.Mocker()
    @patch('redis.StrictRedis.set')
    @patch('redis.StrictRedis.get')
    @patch('redis.StrictRedis.expire')
    @patch('redis.StrictRedis.delete')
    def test_movies_response(self, m, mock_redis_set, mock_redis_get, mock_redis_expire, mock_redis_delete):
        mock_redis_set.side_effect = self.set(test_movies_resp)
        mock_redis_get.side_effect = self.get
        mock_redis_expire.side_effect = self.expire
        mock_redis_delete.side_effect = self.delete

        m.get(self.MOCK_PEOPLE_ADDRESS,
              json=test_people_resp)

        m.get(self.MOCK_MOVIE_ADDRESS_ONE,
              json=test_movies_resp[0])

        m.get(self.MOCK_MOVIE_ADDRESS_TWO,
              json=test_movies_resp[1])

        req = api.movies_response()

        request = self.factory.get('/movies')

        # Test get_movies() as if it were deployed at /movies
        response = get_movies(request)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(req, test_movies_resp)

    @requests_mock.Mocker()
    @patch('redis.StrictRedis.set')
    @patch('redis.StrictRedis.get')
    def test_movies_response_no_result(self, m, mock_redis_set, mock_redis_get):
        mock_redis_set.side_effect = self.set(test_movies_resp)
        mock_redis_get.side_effect = self.get

        m.get(self.MOCK_PEOPLE_ADDRESS,
              json=test_people_resp, status_code=400)

        req = api.movies_response()

        self.assertEqual(req, None)
