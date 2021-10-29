from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import User, Post
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_posts(self, obj):
        return [PostSerializer(post).data for post in obj.post_set.all()]

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
