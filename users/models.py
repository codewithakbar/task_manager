from django.db import models


from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _


from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from .managers import UserManager

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    # rght = models.IntegerField(blank=True, null=True)
    # level = models.IntegerField(blank=True, null=True)
    # lft = models.IntegerField(blank=True, null=True)
    # tree_id = models.IntegerField(blank=True, null=True)
    username = models.CharField(_('username'), max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    profile_image = models.ImageField(upload_to='profile/%Y/%m/%d', null=True, blank=True)
    full_name = models.CharField(max_length=233, null=True, blank=True)
    last_name = models.CharField(max_length=222, null=True, blank=True)
    first_name = models.CharField(max_length=222, null=True, blank=True)
    kasbi = models.CharField(max_length=233, null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    oddiy_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')





class Departaments(MPTTModel):
    title = models.CharField(max_length=233) # Dep name 
    users = models.ManyToManyField(to=CustomUser, related_name="users_dep")
    image = models.ImageField(upload_to='departament/%Y/%m/%d', null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def __str__(self) -> str:
        return self.title



class Notification(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message



