from rest_framework.routers import DefaultRouter
from django.urls import include, path
from watchlist_app.api.views import MovieDetailAV, MovieListAV, ReviewAV, ReviewListAV, ReviewCreateAV, ReviewParticularAV, StreamPlatformAV, UserReview, WatchListAV

# http://127.0.0.1:8000/watch/review/  -> review is same as what is written inside this r``
router = DefaultRouter()
router.register(r'stream', StreamPlatformAV, basename='streamplatform')

urlpatterns = [
    path('list/', MovieListAV.as_view(), name="movie-list"),
    path('<int:pk>/', MovieDetailAV.as_view(), name="movie-details"),
    path('list/test/', WatchListAV.as_view(), name="watchlist-details"),    
    
    path('', include(router.urls)),
    # path('stream/', StreamPlatformListAV.as_view(), name='stream'),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name='stream-detail'),
    
    path('review/', ReviewAV.as_view(), name="review-list"),                                  # User can see all the reviews of all movies
    path('<int:pk>/reviews/', ReviewListAV.as_view(), name="review-detail"),                 # User can see all the reviews of a particular movie
    path('review/<int:pk>/', ReviewParticularAV.as_view(), name="review-specific"),           # User can see a particular review. i.e only one review comment when you open that review
    path('<int:pk>/review-create/', ReviewCreateAV.as_view(), name="review-create"),          # User can create a review for a particular movie, movie will be selected by default

    # path('reviews/<str:username>', UserReview.as_view(), name='user-review-list'),
    path('reviews/', UserReview.as_view(), name='user-review-list'),
]
