from django.db import models

from django.contrib.auth.models import AbstractUser

from rest_framework_simplejwt.tokens import RefreshToken


class CustomUser(AbstractUser):

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    profile_image = models.ImageField(upload_to='profile/%Y/%m/%d', null=True, blank=True)
    full_name = models.CharField(max_length=233, null=True, blank=True)

    oddiy_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username



class Notification(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


