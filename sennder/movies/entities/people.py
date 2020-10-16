from typing import List


class PeopleEntity:
    """People Entity

    People entity data structure
    """

    id = str
    name = str
    films = List[str]

    def __iter__(self, k: List[str]):
        return k

    def __getitem__(self, k: str):
        return ["films"]
