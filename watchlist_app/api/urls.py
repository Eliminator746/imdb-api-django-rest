from django.urls import path
from watchlist_app.api.views import MovieDetailAV, MovieListAV, StreamPlatformDetailAV, StreamPlatformListAV


urlpatterns = [
    path('list/', MovieListAV.as_view(), name="movie-list"),
    path('<int:pk>', MovieDetailAV.as_view(), name="movie-details"),
    path('stream/', StreamPlatformListAV.as_view(), name='stream'),
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail'),
]
