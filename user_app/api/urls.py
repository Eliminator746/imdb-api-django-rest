from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from user_app.api.views import LogoutVS, RegistrationVS

urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='login'),
    path('register/', RegistrationVS.as_view(), name='register'),
    path('logout/', LogoutVS.as_view(), name='logout'),
]
