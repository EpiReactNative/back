from .models import User, Post
from .serializer import UserSerializer, UserDetailSerializer, UserUpdateSerializer, PostSerializer, PostCreationSerializer
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination


class GenericAPIViewset(GenericViewSet):
    """
    Endpoints génériques
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = Serializer

    @action(detail=False, methods=['GET'], serializer_class=UserSerializer)
    def whoami(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)


class UserViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return UserDetailSerializer
        if self.action in ['update']:
            return UserUpdateSerializer
        return UserSerializer

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        users = User.objects.filter(id=pk)
        if len(users) != 1:
            return Response('Unable to find user', status=400)
        user = users[0]
        queryset = User.objects.filter(following=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, many=True)
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
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        users = User.objects.filter(id=pk)
        if len(users) != 1:
            return Response('Unable to find user', status=400)
        user = users[0]
        queryset = user.post_set.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)
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
