from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from watchlist_app.models import StreamPlatform, WatchList
from watchlist_app.serializers import StreamPlatformSerializers, WatchListSerializers

# Complete list
class MovieListAV(APIView):
    
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