from .models import User
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
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
    parser_classes = (MultiPartParser, FormParser)
