from typing import List

from .people import PeopleEntity


class DictMovieEntity:
    id = str
    title = str
    description = str
    release_date = int


class MappedMovieEntity(DictMovieEntity):
    people = List[PeopleEntity]
