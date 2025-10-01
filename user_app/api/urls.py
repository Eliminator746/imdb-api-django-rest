from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from user_app.api.views import LogoutVS, RegistrationVS
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', ObtainAuthToken.as_view(), name='login'),
    path('register/', RegistrationVS.as_view(), name='register'),
    path('logout/', LogoutVS.as_view(), name='logout'),
    
    # JWT Token
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
