import requests

from typing import List
from .cache import RedisCache

redis = RedisCache()
redis_movie_key = "movies"


def get_people() -> list:
    """Get all people

    Makes external request to get all people
    """
    url = "https://ghibliapi.herokuapp.com/people?fields=id,name,films&limit=250"  # noqa: E501
    r = requests.get(url)
    people = r.json()
    return people


def get_movies(movie_url: str) -> object:
    """Return a movie data

    Makes external request to fetch movie data
    """
    r = requests.get(
        f"{movie_url}?fields=id,title,name,description,release_date")

    movie = r.json()
    return movie


def movies_response() -> List[dict]:
    """Return a list of movies

    Method returns a filtered list of movies with their actors
    And saving to cache
    """

    redis_movie_value = redis.get(redis_movie_key)
    if redis_movie_value:
        return redis_movie_value

    movie_urls_hash_store = {}
    structured_movie_data = []
    people = get_people()

    for person in people:
        movies = person["films"]
        if len(movies):
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
                    get_movie_data = get_movies(movie_url)
                    movie = get_movie_data
                    movie["people"] = [person]
                    structured_movie_data.append(movie)
                    movie_urls_hash_store[movie_url] = len(
                        structured_movie_data) - 1

    movie_urls_hash_store = {}

    redis.set(redis_movie_key, structured_movie_data)
    return structured_movie_data


# - Optimal space & time complexity
# O(n) time | O(n) space - where n is the length of the input array
