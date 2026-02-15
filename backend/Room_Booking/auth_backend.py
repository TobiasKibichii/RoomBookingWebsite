from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest


# -------------------------------------------------------------------
# Custom Authentication Backend
# -------------------------------------------------------------------
# This backend allows users to authenticate using their email
# instead of the default username field.
#
# It overrides Django's default ModelBackend authentication logic.
# -------------------------------------------------------------------

class EmailBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticates a user using email and password.

        Parameters:
        - request: The HTTP request object
        - username: Used here as the email value
        - password: Plain-text password to validate

        Returns:
        - User instance if authentication succeeds
        - None if authentication fails
        """
        
        UserModel = get_user_model()

        try:
            # Attempt to retrieve user by email
            user = UserModel.objects.get(email=username)

        except UserModel.DoesNotExist:
            # If no user with this email exists, authentication fails
            return None

        else:
            # Validate the provided password against the stored hash
            if user.check_password(password):
                return user

            # Password did not match
            return None