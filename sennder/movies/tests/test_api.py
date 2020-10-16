# type: ignore
import unittest
import requests_mock

from django.test import RequestFactory
from unittest.mock import patch
from ..services import api
from ..views import get_movies
from .mock_data import (
    test_movie_url,
    test_people_url,
    test_people_resp,
    test_movies_resp,
    test_movie_url_second,
)

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
    MOCK_MOVIE_ADDRESS_ONE = test_movie_url
    MOCK_MOVIE_ADDRESS_TWO = test_movie_url_second

    @requests_mock.Mocker()
    @patch("redis.StrictRedis.set")
    @patch("redis.StrictRedis.get")
    @patch("redis.StrictRedis.expire")
    @patch("redis.StrictRedis.delete")
    def test_movies_response(
        self,
        m,
        mock_redis_set,
        mock_redis_get,
        mock_redis_expire,
        mock_redis_delete,
    ):
        mock_redis_set.side_effect = self.set(test_movies_resp)
        mock_redis_get.side_effect = self.get
        mock_redis_expire.side_effect = self.expire
        mock_redis_delete.side_effect = self.delete

        service = api.MovieService()

        m.get(self.MOCK_PEOPLE_ADDRESS, json=test_people_resp)

        m.get(self.MOCK_MOVIE_ADDRESS_ONE, json=test_movies_resp[0])

        m.get(self.MOCK_MOVIE_ADDRESS_TWO, json=test_movies_resp[1])

        req = service.get_movies_response()

        request = self.factory.get("/movies")

        # Views Test get_movies() as if it were deployed at /movies
        response = get_movies(request)

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(req, test_movies_resp)

    @requests_mock.Mocker()
    @patch("redis.StrictRedis.set")
    @patch("redis.StrictRedis.get")
    @patch("redis.StrictRedis.expire")
    @patch("redis.StrictRedis.delete")
    def test_movies_response_no_result(
        self,
        m,
        mock_redis_set,
        mock_redis_get,
        mock_redis_expire,
        mock_redis_delete,
    ):
        mock_redis_set.side_effect = self.set(test_movies_resp)
        mock_redis_get.side_effect = self.get
        service = api.MovieService()

        m.get(self.MOCK_PEOPLE_ADDRESS, json=test_people_resp, status_code=400)

        req = service.get_movies_response()

        self.assertEqual(req, [])
