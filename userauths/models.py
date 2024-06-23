from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
import phonenumbers
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "User", "user"
        MANAGER = "Manager", "manager"

    email = models.EmailField(unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(
        max_length=15,
        unique=True,
    )
    username = models.CharField(max_length=15, blank=True, null=True)

    base_role = Role.USER
    role = models.CharField(max_length=50, choices=Role.choices, blank=True, null=True)

    USERNAME_FIELD = "telephone"
    REQUIRED_FIELDS = ["first_name", "username"]

    def clean(self):
        super().clean()
        try:
            parsed_number = phonenumbers.parse(self.telephone, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError("Некоректний формату номеру")
            # If you want to store the formatted number, you can do so here
            formatted_number = phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.E164
            )
            self.telephone = formatted_number
        except:
            raise ValidationError("Некоректний формату номеру")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.full_name)


class ManagerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs) -> QuerySet:
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MANAGER)


class Manager(User):
    role = User.Role.MANAGER

    manager = ManagerManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=250, default="")
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.user.full_name} - {self.bio}"


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
