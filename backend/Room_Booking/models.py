from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# -------------------------------------------------------------------
# Room Model
# -------------------------------------------------------------------
# Represents a bookable hotel room.
# Stores room details such as type, pricing, and occupancy limits.
# -------------------------------------------------------------------

class Room(models.Model):

    # Predefined room categories to enforce controlled input
    ROOM_TYPES = [
        ('suite', 'Suite'),
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room')
    ]

    # Supported currencies for pricing
    CURRENCY_TYPES = [
        ('USD', 'USD'),
        ('EUR', 'EUR')
    ]

    name = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(max_length=100, choices=ROOM_TYPES)
    pricePerNight = models.IntegerField(default=150)
    currency = models.CharField(max_length=10, default='USD', choices=CURRENCY_TYPES)
    maxOccupancy = models.IntegerField(default=1)
    description = models.TextField(default=1000)

    def __str__(self):
        # Displayed in Django admin and shell
        return f"{self.name} ({self.type})"


# -------------------------------------------------------------------
# RoomImage Model
# -------------------------------------------------------------------
# Stores images linked to a specific room.
# Relationship: One Room -> Many Images
# -------------------------------------------------------------------

class RoomImage(models.Model):

    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    # Many images can belong to one room.
    # related_name allows reverse access: room.images.all()
    room = models.ForeignKey(
        Room,
        related_name='images',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Image for {self.room.name} - {self.caption or 'No Caption'}"


# -------------------------------------------------------------------
# OccupiedDate Model (Booking)
# -------------------------------------------------------------------
# Represents a booking entry.
# Each record links a room, a user, and a specific date.
# Enforces one booking per room per date.
# -------------------------------------------------------------------

class OccupiedDate(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='occupied_dates'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='booked_dates'
    )

    date = models.DateField()

    class Meta:
        # Prevents double booking:
        # The same room cannot be booked twice on the same date.
        unique_together = ('room', 'date')

    def __str__(self):
        return f"{self.date} - {self.room.name} booked by {self.user.username}"


# -------------------------------------------------------------------
# Custom User Model
# -------------------------------------------------------------------
# Extends Django’s AbstractUser to:
# - Use email as the primary authentication field
# - Add additional fields (e.g., full_name)
# -------------------------------------------------------------------

class User(AbstractUser):

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, default='')

    # Use email instead of username for authentication
    USERNAME_FIELD = 'email'

    # Required when creating a superuser (email replaces username)
    REQUIRED_FIELDS = ['username']