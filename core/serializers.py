from rest_framework import serializers
from .models import MyUser, KeyboardMapping

class MyUserProfileSeralizer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'profile_image']

class KeyboardMappingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = KeyboardMapping
        fields = ['user', 'mappings', 'created_at', 'updated_at', 'is_active']