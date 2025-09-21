from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from watchlist_app.models import Movie
from watchlist_app.serializers import MovieSerializers

# Complete list
class MovieListAV(APIView):
    
    def get(self, request):
        movies= Movie.objects.all()
        serializer=MovieSerializers(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer= MovieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# Individual list    
class MovieDetailAV(APIView):  
      
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)   # get one movie by primary key
            print('movie ', movie)
        except Movie.DoesNotExist:
            return Response(
                {'error': "No movie found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = MovieSerializers(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie=Movie.objects.get(pk=pk)
        serializer=MovieSerializers(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        movie= Movie.objects.get(pk=pk)
        movie.delete()
        return Response()
     
        
        
        