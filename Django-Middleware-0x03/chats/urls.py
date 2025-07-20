

from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from . import views

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('test/', views.test_view, name='test'),
    path('', include(router.urls)),
]

# routers.DefaultRouter() NestedDefaultRouter