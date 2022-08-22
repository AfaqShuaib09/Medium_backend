from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import mixins, viewsets, generics, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user_accounts.serializer import RegisterSerializer, UserSerializer, ChangePasswordSerializer

# Create your views here.
class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    This view provides a post request to register a user.
    """
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        """
        Handles the request to register/create a user.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })

class LoginViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    This view provides a post request to login a user.
    """
    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        """
        Handles the request to login a user.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AuthToken.objects.create(user)[1]
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': token
        })

class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """
    API endpoint that allows all users to be viewed or a single user by passing the id.\n
    GET -> list all users -> /api/users/ \n
    GET -> list a single user -> /api/users/id/
    """
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


class ChangePasswordViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
    API endpoint that allows users to change their password.
    """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        """
        Handles the request to change a user's password.
        """
        instance = self.get_object()
        if not instance.check_password(request.data['old_password']):
            return Response({'old_password': 'Wrong password.'}, status=status.HTTP_400_BAD_REQUEST)
        instance.set_password(request.data['new_password'])
        instance.save()
        return Response({'success': 'Password changed successfully.'}, status=status.HTTP_200_OK)
