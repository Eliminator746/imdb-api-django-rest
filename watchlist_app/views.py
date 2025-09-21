# from watchlist_app.models import Movie
# from rest_framework.response import Response
# from .serializers import MovieSerializers
# from rest_framework.decorators import api_view
# from rest_framework import status

# # Create your views here.

# # CRUD operation
# @api_view(['GET', 'POST'])
# def movie_list(request):
    
#     if request.method == 'GET':
#         movies= Movie.objects.all()
#         serializer=MovieSerializers(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer= MovieSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
       

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request,pk):
    
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)   # get one movie by primary key
#             print('movie ', movie)
#         except Movie.DoesNotExist:
#             return Response(
#                 {'error': "No movie found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         serializer = MovieSerializers(movie)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         movie=Movie.objects.get(pk=pk)
#         serializer=MovieSerializers(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     if request.method == 'DELETE':
#         movie= Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response()
     