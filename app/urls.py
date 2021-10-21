from django.urls import path, include
from rest_framework import routers
from .views import UserViewset, GenericAPIViewset

router = routers.DefaultRouter()
router.register(r'api', GenericAPIViewset, basename='Generic Endpoints')
router.register(r'user', UserViewset, basename='Users')

urlpatterns = [
    path('', include(router.urls)),
]
