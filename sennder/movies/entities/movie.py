from typing import List

from .people import PeopleEntity


class DictMovieEntity:
    """Movie Entity

    Single movie entity data structure
    """

    id = str
    title = str
    description = str
    release_date = int

    def __setitem__(self, k, v):
        return self


class MappedMovieEntity(DictMovieEntity):
    """Mapped Movie Entity

    List of movies entity data structure
    """

    people = List[PeopleEntity]
