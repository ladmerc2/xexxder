from django.shortcuts import render

from .services import api  # type: ignore


def get_movies(request):
    movieService = api.MovieService()
    get_movies = movieService.get_movies_response()
    return render(request, "movies/movies.html", {"movies": get_movies})
