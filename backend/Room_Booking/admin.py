from django.contrib import admin
from .models import Room, RoomImage, OccupiedDate, User


# -------------------------------------------------------------------
# Django Admin Configuration
# -------------------------------------------------------------------
# This file registers application models with Django’s admin site,
# allowing administrators to manage database records through
# the built-in admin interface.
# -------------------------------------------------------------------


# Register Room model
# Enables CRUD operations for rooms in the admin dashboard.
admin.site.register(Room)


# Register custom User model
# Since the project uses a custom user model (email-based login),
# it must be explicitly registered.
admin.site.register(User)


# Register RoomImage model
# Allows administrators to manage room images and captions.
admin.site.register(RoomImage)


# Register OccupiedDate model
# Enables viewing and managing booking records.
admin.site.register(OccupiedDate)