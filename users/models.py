from django.db import models

from django.contrib.auth.models import AbstractUser

from rest_framework_simplejwt.tokens import RefreshToken


class CustomUser(AbstractUser):


    email = models.EmailField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

