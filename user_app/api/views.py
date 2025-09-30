from django.contrib.auth.models import User
from rest_framework import generics
from user_app.api.serializers import RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from user_app import models

class RegistrationVS(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    
    def create(self, request):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {}
        account = serializer.save()
        
        data['response'] = 'Registration Successfull!'
        data['username'] = account.username
        data['email'] = account.email
        
        # Generate token automatically -> We do via using signal
        token = Token.objects.get(user=account)
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)

class LogoutVS(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request):
        try:
            token = Token.objects.get(user = request.user)
            token.delete()
            
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
            
        except Token.DoesNotExist:
            return Response({
                'error': 'Token not found'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    