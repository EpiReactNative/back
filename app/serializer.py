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

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        password = user.password
        user.set_password(password)
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
        return [PostSerializer(post).data['id'] for post in obj.post_set.all()]

    def get_followers(self, obj):
        return [UserSerializer(user).data['id'] for user in User.objects.filter(following=obj)]

    def get_following(self, obj):
        return [UserSerializer(user).data['id'] for user in obj.following.all()]


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostCreationSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Post
        exclude = ('author',)

    def create(self, validated_data):
        image = validated_data.pop('image')
        caption = validated_data.pop('caption')
        return Post.objects.create(image=image, caption=caption, author=self.context['request'].user)
