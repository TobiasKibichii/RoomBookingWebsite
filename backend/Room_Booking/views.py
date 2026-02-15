from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Room, OccupiedDate, User
from .serializers import RoomSerializer, OccupiedDateSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


# -------------------------------------------------------------------
# API Root
# -------------------------------------------------------------------
# Entry point of the API.
# Provides discoverable links to main resources.
# -------------------------------------------------------------------

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'rooms': reverse('room-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'occupied-dates': reverse('occupieddate-list', request=request, format=format)
    })


# -------------------------------------------------------------------
# Room Views
# -------------------------------------------------------------------
# Handles listing, creation, retrieval, update, and deletion of rooms.
# Only admins can modify rooms. All users can read.
# -------------------------------------------------------------------

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


# -------------------------------------------------------------------
# Booking Views (Occupied Dates)
# -------------------------------------------------------------------
# Represents room bookings.
# Enforces:
# - Authenticated users can create bookings
# - Users can only view their own bookings (unless admin)
# - Booking ownership restrictions on update/delete
# -------------------------------------------------------------------

class OccupiedDatesList(generics.ListCreateAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Restrict regular users to only see their own bookings.
        Admins and superusers can view all bookings.
        """
        user = self.request.user

        if not user.is_superuser and not user.is_staff:
            return OccupiedDate.objects.filter(user=user)

        return super().get_queryset()

    def perform_create(self, serializer):
        """
        Automatically assign the currently authenticated user
        as the booking owner.
        Prevents users from creating bookings on behalf of others.
        """
        serializer.save(user=self.request.user)


class OccupiedDatesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OccupiedDate.objects.all()
    serializer_class = OccupiedDateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# -------------------------------------------------------------------
# User Views
# -------------------------------------------------------------------
# Provides user listing and retrieval.
# Enforces:
# - Users can only see their own data
# - Admins can see all users
# -------------------------------------------------------------------

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Admins can view all users.
        Regular users can only view their own account.
        """
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return User.objects.all()

        return User.objects.filter(id=user.id)


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """
        Ensures users can only access:
        - Their own profile
        - Or any profile if they are admin/staff
        """
        user = self.request.user
        obj = super().get_object()

        if obj == user or user.is_staff or user.is_superuser:
            return obj

        raise PermissionDenied("You do not have permission to view this user.")


# -------------------------------------------------------------------
# Authentication Views
# -------------------------------------------------------------------
# Handles registration and login.
# Uses token authentication.
# -------------------------------------------------------------------

class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Registers a new user and immediately generates an auth token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name
            },
            "token": token.key
        }, status=201)


class Login(APIView):
    """
    Authenticates user credentials and returns an existing or new token.
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid username or password')

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.email,
                "email": user.email,
                "full_name": user.full_name
            },
            "token": token.key
        })