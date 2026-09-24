from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager

from apps.core.models import TimestampedModel


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        verbose_name='شماره تماس',
    )

    is_admin = models.BooleanField(
        default=False,
        verbose_name="ادمین؟",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال؟",
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self) -> str:
        return self.phone_number

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
