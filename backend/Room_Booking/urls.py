from django.urls import path
from Room_Booking import views
from rest_framework.urlpatterns import format_suffix_patterns


# -------------------------------------------------------------------
# URL Configuration
# -------------------------------------------------------------------
# This file maps URL paths to their corresponding view classes.
# It defines the public API structure of the application.
#
# Each endpoint follows RESTful conventions:
# - Collection endpoints (e.g., /rooms/)
# - Detail endpoints (e.g., /rooms/<id>/)
# -------------------------------------------------------------------

urlpatterns = [

    # API Root (Entry point)
    # Provides navigable links to main resources
    path('', views.api_root, name='api-root'),

    # -------------------------
    # Room Endpoints
    # -------------------------

    # List all rooms or create a new room (Admin only for POST)
    path('rooms/', views.RoomList.as_view(), name='room-list'),

    # Retrieve, update, or delete a specific room by primary key
    path('rooms/<int:pk>/', views.RoomDetail.as_view(), name='room-detail'),

    # -------------------------
    # Booking (Occupied Dates) Endpoints
    # -------------------------

    # List bookings or create a new booking
    path('occupied-dates/', views.OccupiedDatesList.as_view(), name='occupieddate-list'),

    # Retrieve, update, or delete a specific booking
    path('occupied-dates/<int:pk>/', views.OccupiedDatesDetail.as_view(), name='occupieddate-detail'),

    # -------------------------
    # User Endpoints
    # -------------------------

    # List users (restricted by permissions)
    path('users/', views.UserList.as_view(), name='user-list'),

    # Retrieve a specific user
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),

    # -------------------------
    # Authentication Endpoints
    # -------------------------

    # Login endpoint (returns authentication token)
    path('login/', views.Login.as_view(), name='login'),

    # User registration endpoint
    path('register/', views.Register.as_view(), name='register'),
]


# -------------------------------------------------------------------
# Format Suffix Support
# -------------------------------------------------------------------
# Allows clients to specify response format in the URL.
# Example:
# - /rooms.json
# - /rooms.api
#
# This is optional but improves API flexibility.
# -------------------------------------------------------------------

urlpatterns = format_suffix_patterns(urlpatterns)