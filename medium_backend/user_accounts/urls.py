''' urls definition for user accounts app '''
from django.urls import include, path
from knox import views as knox_views
from rest_framework.routers import DefaultRouter

from user_accounts.views import (ChangePasswordViewSet, LoginViewSet,
                                 ProfileViewSet, RegisterViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('forgot-password/', include('django_rest_passwordreset.urls', namespace='forgot_password')),
]
