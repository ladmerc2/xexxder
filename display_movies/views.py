from .services import api
from django.shortcuts import render


def get_movies(request):
    get_movies = api.movies_response()
    return render(request, "display_movies/movies.html", {
        "movies": get_movies
    })
