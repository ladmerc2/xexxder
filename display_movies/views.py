from .services import api
from django.shortcuts import render

# Create your views here.


async def get_movies(request):
    # View code here...
    get_movies = api.movies_response()
    return render(request, 'display_movies/movies.html', {
        'movies': get_movies
    })
