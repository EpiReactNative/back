import os
import uuid
import base64

from .misc import *
from .models import User, Post, DEFAULT_PROFILE_PICTURE
from .serializer import UserSerializer, UserDetailSerializer, PostSerializer, PostCreationSerializer
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes


class GenericAPIViewset(GenericViewSet):
    """
    Endpoints génériques
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = Serializer

    @action(detail=False, methods=['GET'], serializer_class=UserDetailSerializer)
    def whoami(self, request):
        serializer = UserDetailSerializer(
            request.user, context={'request': request})
        return Response(serializer.data)


class UserViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return UserDetailSerializer
        return UserSerializer

    def update(self, request, pk, format=None, partial=True):
        queryset = self.get_queryset().filter(id=pk)
        if not len(queryset):
            return Response(status.HTTP_404_NOT_FOUND)
        user = queryset[0]
        if 'username' in request.data:
            user.username = request.data['username']
        if 'email' in request.data:
            user.email = request.data['email']
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'bio' in request.data:
            user.bio = request.data['bio']
        if 'password' in request.data:
            user.set_password(request.data['password'])
        if 'profile_picture' in request.data:
            header, base64_data = request.data['profile_picture'].split(
                ';base64,')
            decoded_file = base64.b64decode(base64_data)
            file_name = str(uuid.uuid4())
            file_extension = get_file_extension(file_name, decoded_file)
            if user.profile_picture and user.profile_picture.name != DEFAULT_PROFILE_PICTURE:
                if os.path.isfile(user.profile_picture.path):
                    os.remove(user.profile_picture.path)
            user.profile_picture = ContentFile(
                decoded_file, name=file_name + '.' + file_extension)
        user.save()
        return Response(status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        users = User.objects.filter(id=pk)
        if len(users) != 1:
            return Response('Unable to find user', status=400)
        user = users[0]
        queryset = User.objects.filter(following=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(reversed(page), many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(reversed(queryset), many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        users = User.objects.filter(id=pk)
        if len(users) != 1:
            return Response('Unable to find user', status=400)
        user = users[0]
        queryset = user.following.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(reversed(page), many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(reversed(queryset), many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        users = User.objects.filter(id=pk)
        if len(users) != 1:
            return Response('Unable to find user', status=400)
        user = users[0]
        queryset = user.author.all().order_by('-created_at')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostSerializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        users = User.objects.filter(id=pk)
        if len(users) != 1:
            return Response('Unable to find user', status=400)
        user = users[0]
        queryset = user.likes.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostSerializer(
                reversed(page), many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(
            reversed(queryset), many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], serializer_class=None)
    def follow(self, request, pk=None):
        parser_classes = JSONParser
        queryset = self.get_queryset()
        users = queryset.filter(id=pk)
        if len(users) != 1:
            return Response('Unable to find user', status=400)
        user = users[0]
        if request.user.following.filter(id=user.id).exists():
            request.user.following.remove(user.id)
        else:
            request.user.following.add(user.id)
        user.save()
        serializer = UserDetailSerializer(
            request.user, context={'request': request})
        return Response(serializer.data)


class PostViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreationSerializer
        return PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'create':
            context.update({"request": self.request})
        return context

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        queryset = self.get_queryset()
        posts = queryset.filter(id=pk)
        if len(posts) != 1:
            return Response('Unable to find post', status=400)
        post = posts[0]
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        queryset = self.get_queryset()
        posts = queryset.filter(id=pk)
        if len(posts) != 1:
            return Response('Unable to find post', status=400)
        post = posts[0]
        users = post.likes.all()

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = UserSerializer(
                reversed(page), many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(reversed(users), many=True, context={'request': request})
        return Response(serializer.data)
