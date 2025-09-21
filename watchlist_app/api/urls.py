from django.urls import path
from watchlist_app.api.views import MovieDetailAV, MovieListAV


urlpatterns = [
    path('list/', MovieListAV.as_view(), name="movie-list"),
    path('<int:pk>', MovieDetailAV.as_view(), name="movie-details"),
]
