from rest_framework import serializers
from watchlist_app.models import StreamPlatform, WatchList

class WatchListSerializers(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = '__all__'
    
    # Validation
    def validate(self, data):
        if len(data['title']) < 2:
            raise serializers.ValidationError({"title": "Title must be at least 2 characters long."})
        return data
    
    # Create, Update 
    def create(self, validated_data):
        return WatchList.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.storyline = validated_data.get('storyline', instance.storyline)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    def get_len_name(self, object):
        return len(object.title)
    
class StreamPlatformSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        
    def create(self, validated_data):
        return StreamPlatform.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.about = validated_data.get('about', instance.about)
        instance.website = validated_data.get('website', instance.website)
        instance.save()
        return instance
        