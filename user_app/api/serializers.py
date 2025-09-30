from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField( style={'input-type' : 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},   # Do not include password in responses
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'p1 and p2 are not same'})
        
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'This email already exists!'})
        
        account = User(username=self.validated_data['username'], email=self.validated_data['email'])
        
        # Set and hash the password securely
        account.set_password(password)
        
        # Save the user to the database
        account.save()
        return account
