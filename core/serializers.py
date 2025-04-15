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
        fields = ['id', 'user', 'name', 'description','mappings', 'created_at', 'updated_at', 'is_active']

class RegisterUserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    class Meta:
        model = MyUser
        fields= ['username', 'email', 'password']
        
    def create(self, validated_data):
        user = MyUser(
            username = validated_data["username"],
            email = validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user