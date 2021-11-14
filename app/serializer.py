from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import User, Post
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'profile_picture', 'bio', ]

    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_posts(self, obj):
        return [int(post) for post in obj.author.all()]

    def get_followers(self, obj):
        return [int(user) for user in User.objects.filter(following=obj)]

    def get_following(self, obj):
        return [int(user) for user in obj.following.all()]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_author(self, obj):
        return UserSerializer(obj.author, context={'request': self.context['request']}).data


class PostCreationSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Post
        exclude = ('author', 'height', 'width',)

    def create(self, validated_data):
        image = validated_data.pop('image')
        caption = validated_data.pop('caption')
        return Post.objects.create(image=image, caption=caption, author=self.context['request'].user)
