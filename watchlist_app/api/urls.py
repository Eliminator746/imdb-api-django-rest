from django.urls import path
from watchlist_app.api.views import MovieDetailAV, MovieListAV, ReviewAV, ReviewDetailAV, ReviewListAV, ReviewCreateAV, ReviewParticularAV, StreamPlatformDetailAV, StreamPlatformListAV


urlpatterns = [
    path('list/', MovieListAV.as_view(), name="movie-list"),
    path('<int:pk>', MovieDetailAV.as_view(), name="movie-details"),
    path('stream/', StreamPlatformListAV.as_view(), name='stream'),
    path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail'),
    
    path('stream/review', ReviewAV.as_view(), name="review-list"),                                  # User can see all the reviews of all movies
    path('stream/<int:pk>/review', ReviewDetailAV.as_view(), name="review-detail"),                 # User can see all the reviews of a particular movie
    path('stream/review/<int:pk>', ReviewParticularAV.as_view(), name="review-specific"),           # User can see a particular review. i.e only one review comment when you open that review
    path('stream/<int:pk>/review-create', ReviewCreateAV.as_view(), name="review-create"),          # User can create a review for a particular movie, movie will be selected by default
]
