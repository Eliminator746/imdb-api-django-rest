from rest_framework import serializers
from watchlist_app.models import Review, StreamPlatform, WatchList

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = '__all__'
        exclude = ['watchlist']
    
class WatchListSerializers(serializers.ModelSerializer):
    review = ReviewSerializers(many=True, read_only=True)
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
        if len(data['name']) < 2:
            raise serializers.ValidationError({"name": "name must be at least 2 characters long."})
        return data
    
