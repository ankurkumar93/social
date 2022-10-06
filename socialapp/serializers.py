from rest_framework import serializers
from .models import User, Post

class UserLoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'password']
