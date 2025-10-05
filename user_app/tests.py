from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationTest(APITestCase):
    
    def test_register(self):
        
        data = {
            "username": "test123",
            "email": "test@gamil.com",
            "password": "pass",
            "password2" : "pass"
        }
    
        response = self.client.post(reverse('register'),  data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginLogoutTest(APITestCase):
    
    def setUp(self):
        # Create temporary User
        self.user = User.objects.create_user(username="example", password="newPassword@123")

        # Creating token and it to Header
        self.token = Token.objects.get(user__username='example')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_login(self):
        
        data = {
            "username": "example",
            "password": "newPassword@123"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        response = self.client.delete(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
