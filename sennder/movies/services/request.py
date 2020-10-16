import requests


class RequestService:
    def make_get_request(url, params):
        """Make GET request

        Makes external request to get data
        """
        r = requests.get(url, params=params)
        return r
