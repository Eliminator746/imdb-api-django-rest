from django.db import models

# Create your models here.
class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=50)
    website = models.URLField(max_length=150)
    
    def __str__(self):
        return self.name
    
# A StreamPlatform (like Netflix, Amazon Prime) can have many WatchList (movies/shows).
class WatchList (models.Model):
    title = models.CharField(max_length=500)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist", null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    