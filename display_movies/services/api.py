import os
import requests
import asyncio

from typing import Dict, List, Tuple


def get_people() -> list:
    url = 'https://ghibliapi.herokuapp.com/people?fields=id,name,films&limit=250'
    r = requests.get(url)
    people = r.json()
    return people


def get_movies(movie_url: str) -> object:
    r = requests.get(
        f'{movie_url}?fields=id,title,name,description,release_date')
    movie = r.json()
    return movie


def movies_response() -> List[dict]:
    movie_urls_hash_store = {}
    structured_movie_data = []
    people = get_people()

    for person in people:
        movies = person['films']
        if len(movies):
            for idx, movie_url in enumerate(movies):
                # get_movies
                if movie_url in movie_urls_hash_store:
                    # skip adding to hash but add person to movie list via index
                    movie_url_index_value = movie_urls_hash_store[movie_url]
                    # O(1)T
                    movie = structured_movie_data[movie_url_index_value]
                    # if person[films] has movie id then add
                    person_movie_id = movie_url.split('/')[-1]
                    if person_movie_id == movie['id']:
                        movie['people'].append(person)
                        structured_movie_data[movie_url_index_value] = movie
                else:
                    # then add new movie w/ person to list
                    get_movie_data = get_movies(movie_url)
                    movie = get_movie_data
                    movie['people'] = [person]
                    structured_movie_data.append(movie)
                    movie_urls_hash_store[movie_url] = len(
                        structured_movie_data) - 1
    movie_urls_hash_store = {}  # reset in memory

    return structured_movie_data

# - Optimal space & time complexity
# O(n) time | O(n) space - where n is the length of the input array
