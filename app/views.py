from .models import User
from .serializer import UserSerializer
from rest_framework.serializers import Serializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

class GenericAPIViewset(GenericViewSet):
    """
    Endpoints génériques
    """
    serializer_class = Serializer

class UserViewset(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
