import requests  # type: ignore

from typing import Mapping, Union


class RequestService:
    def make_get_request(
        self, url: str, params: Mapping[str, Union[str, int]]
    ):
        """Make GET request

        Makes external request to get data
        """
        r = requests.get(url, params=params)
        return r
