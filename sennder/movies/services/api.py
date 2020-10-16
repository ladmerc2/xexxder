from typing import List

from django.conf import settings
from .cache import RedisCache
from .request import RequestService
from ..entities import (
    people as PEntity,
    movie as MEntity,
)


class MovieService:

    BASE = settings.MOVIE_BASE_API_URL

    def __init__(self):
        self.redis = RedisCache()
        self.redis_movie_key = "movies"
        self.request = RequestService

    def get_people(self) -> list:
        """Get all people

        Request to get all people
        """
        url = f"{self.BASE}people"
        params = {"fields": "id,name,films", "limit": 250}
        r = self.request.make_get_request(url, params)

        if r.status_code != 200:
            # use proper logger here
            return []
        people = r.json()
        return people

    def get_movies(self, movie_url: str) -> MEntity.DictMovieEntity:
        """Return a movie data

        Makes external request to fetch movie data
        """

        params = {"fields": "id,title,description,release_date"}
        r = self.request.make_get_request(movie_url, params)
        if r.status_code != 200:
            # use proper logger here
            return {}
        movie = r.json()
        return movie

    def get_movies_response(self) -> List[dict]:
        """Return a list of movies

        Method returns a filtered list of movies with their actors
        And saving to cache
        """

        redis_movie_value = self.redis.get(self.redis_movie_key)
        if redis_movie_value:
            return redis_movie_value
        people = self.get_people() or []
        print(len(people))  # remove this later

        return self.map_person_to_movies(people)

    def map_person_to_movies(
        self,
        people: List[PEntity.PeopleEntity],
    ) -> List[MEntity.MappedMovieEntity]:
        """Perform mapping logic

        Method to map persons to movies
        """

        movie_urls_hash_store = {}
        structured_movie_data = []

        for person in people:
            movies = person["films"]
            for idx, movie_url in enumerate(movies):
                if movie_url in movie_urls_hash_store:
                    # skip adding to hash
                    # but add person to movie list via index
                    movie_url_index_value = movie_urls_hash_store[movie_url]
                    movie = structured_movie_data[movie_url_index_value]

                    # if person[films] has movie id then add
                    person_movie_id = movie_url.split("/")[-1]
                    if person_movie_id == movie["id"]:
                        movie["people"].append(person)
                        structured_movie_data[movie_url_index_value] = movie
                else:
                    # then add new movie w/ person to list
                    get_movie_data = self.get_movies(movie_url)
                    if get_movie_data:
                        movie = get_movie_data
                        movie["people"] = [person]
                        structured_movie_data.append(movie)
                        movie_urls_hash_store[movie_url] = (
                            len(structured_movie_data) - 1
                        )

        movie_urls_hash_store = {}

        self.redis.set(self.redis_movie_key, structured_movie_data)
        return structured_movie_data


# - Optimal space & time complexity
# O(n) time | O(n) space - where n is the length of the input array
