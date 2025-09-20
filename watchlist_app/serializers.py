from rest_framework import serializers
from .models import Movie

class MovieSerializers(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    description=serializers.CharField()
    active=serializers.BooleanField()
    
    # Validation
    def validate(self, data):
        if len(data['name']) < 2:
            raise serializers.ValidationError({"name": "Name must be at least 2 characters long."})
        return data
    
    # Create, Update 
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance