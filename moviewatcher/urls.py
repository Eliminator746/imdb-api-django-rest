from django.contrib import admin
from django.urls import path, include

# Donot write imports here when you're using include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie/', include('watchlist_app.api.urls'))
]
