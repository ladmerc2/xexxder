# type: ignore
import unittest
import requests_mock


from ..services import api
from .mock_data import (
    test_people_url,
    test_people_resp,
)


class TestGetPeople(unittest.TestCase):

    MOCK_ADDRESS = test_people_url

    @requests_mock.Mocker()
    def test_people(self, m):
        service = api.MovieService()
        m.get(self.MOCK_ADDRESS, json=test_people_resp)
        req = service.get_people()

        self.assertEqual(len(req), len(test_people_resp))
        self.assertEqual(req[0]["name"], "Ashitaka")

    @requests_mock.Mocker()
    def test_people_bad_request(self, m):
        service = api.MovieService()
        m.get(self.MOCK_ADDRESS, json=test_people_resp, status_code=400)
        req = service.get_people()

        self.assertEqual(req, [])
