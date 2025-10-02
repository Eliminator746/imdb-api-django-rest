from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
# from watchlist_app.api.throttling import ReviewListThrottle, ReviewParticularThrottle
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from watchlist_app.models import Review, StreamPlatform, WatchList
from watchlist_app.serializers import ReviewSerializers, StreamPlatformSerializers, WatchListSerializers

# Complete list
class MovieListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request):
        movies= WatchList.objects.all()
        serializer=WatchListSerializers(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer= WatchListSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# Individual list    
class MovieDetailAV(APIView):  
    permission_classes = [AdminOrReadOnly]
      
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            print('movie ', movie)
        except WatchList.DoesNotExist:
            return Response(
                {'error': "No movie found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = WatchListSerializers(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie=WatchList.objects.get(pk=pk)
        serializer=WatchListSerializers(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        movie= WatchList.objects.get(pk=pk)
        movie.delete()
        return Response()
     
# StreamPlatform
# Complete List        

class StreamPlatformListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializers(platform, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)

class StreamPlatformDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"error": "Platform not found"}, status=404)

        serializer = StreamPlatformSerializers(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            serializer = StreamPlatformSerializers(platform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Platform not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
# ---------------------------------------------------------------------------------------------------------------------------------
#                  ViewSet : CRUD [ old way ]
# ---------------------------------------------------------------------------------------------------------------------------------  
# class StreamPlatformAV(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializers(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializers(watchlist)
#         return Response(serializer.data)
    
#     def create(self, request):
#         serializer = StreamPlatformSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
      
# ---------------------------------------------------------------------------------------------------------------------------------
#                  ModelViewSet : CRUD [ least code ]
# ---------------------------------------------------------------------------------------------------------------------------------  
class StreamPlatformAV(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializers            
# ---------------------------------------------------------------------------------------------------------------------------------  

# Review System
# ---------------------------------------------------------------------------------------------------------------------------------
#                   User can see all the reviews of all movies
# ---------------------------------------------------------------------------------------------------------------------------------
class ReviewAV(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    
# ---------------------------------------------------------------------------------------------------------------------------------
#                   User can see all the reviews of a particular movie
# ---------------------------------------------------------------------------------------------------------------------------------
class ReviewListAV(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        pk= self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)

# ---------------------------------------------------------------------------------------------------------------------------------
#                   User can create a review for a particular movie, movie will be selected by default
# ---------------------------------------------------------------------------------------------------------------------------------
# 1. Get the pk from URL
# 2. Find that review from Watchlist, which is a connected Modal
# 3. Checks if user has reviewed THIS specific movie - [EDGE CASES]
# 4. Save it to watchlist, which is defined in Review Modal
# ---------------------------------------------------------------------------------------------------------------------------------
        
class ReviewCreateAV(generics.CreateAPIView):
    serializer_class= ReviewSerializers
    permission_classes= [IsAuthenticated]
    
    def get_queryset(self):
        return Review.objects.all()

    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            raise ValidationError(f"WatchList with ID {pk} does not exist!")
        review_user=self.request.user
        
        # Checks if user has reviewed THIS specific movie
        review_queryset = Review.objects.filter(
            watchlist=movie,
            review_user=review_user
        )
        
        if review_queryset.exists():
            raise ValidationError("You've already reviewed this show!")
        
        # Adding review count + avg here
        rating = serializer.validated_data['rating']
        if movie.number_rating == 0:
            movie.avg_rating = rating
        else:
            total =  (movie.avg_rating * movie.number_rating) + rating
            movie.avg_rating = total / (movie.number_rating + 1)
        
        movie.number_rating = movie.number_rating + 1
        movie.save()
        serializer.save(watchlist = movie, review_user = review_user)        
        
# ---------------------------------------------------------------------------------------------------------------------------------
#                   User can see a particular review. i.e only one review comment when you open that review
# ---------------------------------------------------------------------------------------------------------------------------------

class ReviewParticularAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    # throttle_classes = [ReviewParticularThrottle]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    
    def perform_update(self, serializer):
        # pk = self.kwargs['pk']
        # movie = Review.objects.get(pk=pk).watchlist     
         
        review = serializer.instance       # Review being updated
        movie = review.watchlist           # Related WatchList
        
        print(serializer)
        print("----------")
        print(review)
        print("----------")
        print(movie)
        
        old_rating = review.rating
        new_rating = serializer.validated_data['rating']
    
        total = movie.avg_rating * movie.number_rating
        total = total - old_rating + new_rating
        movie.avg_rating = total / movie.number_rating
        
        movie.save()
        # serializer.save(watchlist = movie, review_user =' review_user')
        serializer.save()