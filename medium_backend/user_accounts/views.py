from email.policy import default
import profile
from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import generics, mixins, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from user_accounts.models import Profile
from user_accounts.permissions import IsOwnerOrReadOnly, IsNonAuthenticated
from user_accounts.serializer import (ChangePasswordSerializer,
                                      ProfileSerializer, RegisterSerializer,
                                      UpdateProfileSerializer, UserSerializer)


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
    permission_classes = (AllowAny, IsNonAuthenticated)

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
    Retrieve:
        Return a user instance.
    
    List:
        Return all users, if the user is admin.
    """
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """ Allow list-all users only to admin users. """
        return (IsAdminUser(),) if self.action == 'list' else (IsAuthenticated(),)


class ChangePasswordViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """
    API endpoint that allows users to change their password.
    """
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["put"]

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


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, created, updated or deleted.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__username'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
        Create a new profile associated with the user.
        """
        try:
            user = User.objects.get(username=request.data['username'])
            if Profile.objects.filter(user__username=user.username).exists():
                return Response({"message": "Profile already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'User not found'}, status=404)

        user_profile = Profile.objects.create(user=user,
                            full_name=request.data.get('full_name', ''),
                            cnic=request.data.get('cnic', ''),
                            contact_number=request.data.get('contact_number', ''),
                            address=request.data.get('address', ''),
                            gender = request.data.get('gender', 'Do not specify'),
                            country = request.data.get('country', 'PK'),
                            profile_pic = request.data.get('profile_pic', None),
                            bio = request.data.get('bio', ''),
                        )
        user_profile.save()
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



    def get_serializer_class(self):
        """
        Returns the serializer class for the viewset
        """
        return UpdateProfileSerializer if self.action == 'update' else self.serializer_class
