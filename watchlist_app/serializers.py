from rest_framework import serializers
from watchlist_app.models import StreamPlatform, WatchList

class WatchListSerializers(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = '__all__'
    
    def validate(self, data):
        if len(data['title']) < 2:
            raise serializers.ValidationError({"title": "Title must be at least 2 characters long."})
        return data
    
    def get_len_name(self, object):
        return len(object.title)
    
class StreamPlatformSerializers(serializers.ModelSerializer):
     
    watchlist = WatchListSerializers(many=True, read_only=True)    
    class Meta:
        model = StreamPlatform
        fields = '__all__'
    
    def validate(self, data):
        if len(data['title']) < 2:
            raise serializers.ValidationError({"title": "Title must be at least 2 characters long."})
        return data