from .models import Post, Comment, Like
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_content(self, value):
        if len(value) < 1000:
            raise serializers.ValidationError("Content must be at least 10 characters long.")
        return value

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'post', 'author', 'created_at']

    def validate_content(self, value):
        if len(value) < 400:
            raise serializers.ValidationError("Comment must be at least 10 characters long.")
        return value

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
    

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'post', 'user', 'created_at']

    def create(self, validated_data):
        return Like.objects.create(**validated_data)
    
    def validate(self, data):
        if Like.objects.filter(post=data['post'], user=data['user']).exists():
            raise serializers.ValidationError("You have already liked this post.")
        return data
    
from rest_framework import serializers
from .models import Emoji

class EmojiSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Emoji
        fields = ['id', 'name', 'unicode', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']