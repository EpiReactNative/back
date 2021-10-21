from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from .views import UserViewset, GenericAPIViewset

router = routers.DefaultRouter()
router.register(r'api', GenericAPIViewset, basename='Generic Endpoints')
router.register(r'user', UserViewset, basename='Users')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token)
]
