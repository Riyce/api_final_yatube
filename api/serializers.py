from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField( 
        slug_field='username', 
        queryset = User.objects.all(),
        default=serializers.CurrentUserDefault()
    ) 
    following = serializers.SlugRelatedField( 
        slug_field='username', 
        queryset = User.objects.all(),
    )

    def validate(self, data):
        if data['user'] == data['following']:
            raise serializers.ValidationError('Вы не можете подписываться на самого себя!')
        if Follow.objects.filter(user=data['user'], following=data['following']).exists():
            raise serializers.ValidationError('Такая подписка уже существует!')
        return data

    class Meta:
        fields = '__all__'
        model = Follow
