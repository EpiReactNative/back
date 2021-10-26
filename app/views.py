from .models import User, Post
from .serializer import UserSerializer, PostSerializer, PostCreationSerializer
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated


class GenericAPIViewset(GenericViewSet):
    """
    Endpoints génériques
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = Serializer

    @action(detail=False, methods=['GET'], serializer_class=UserSerializer)
    def whoami(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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

    # def create(self, request, *args, **kwargs):
    #     serializer = PostCreationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(author=User.objects.filter(id=1))
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)

    # def perform_create(self, serializer):
    #     print('hey ' + self.request.user.username + '!')
    #     # serializer.save()
    #     serializer.save(author=self.request.user)
