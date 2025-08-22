from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate



class UserRegistration(serializers.ModelSerializer):
     password = serializers.CharField(write_only=True)
     confirm_password = serializers.CharField(write_only=True)  # ✅ extra field

     class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

     def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

     def create(self, validated_data):
        validated_data.pop('confirm_password')  # remove before creating user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
        
     def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
     def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
     def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
     def validate_profile_picture(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError("Profile picture size must be less than 2MB")
        return value
     def validate_bio(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Bio must be less than 500 characters")
        return value
     def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    

        
     def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")