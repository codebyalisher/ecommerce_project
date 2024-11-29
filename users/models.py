from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from uuid import uuid4
from django.utils import timezone
from django.utils.timezone import  now
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, related_name="groups")

class Userm(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    groups = models.ManyToManyField('auth.Group', related_name="users")
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # Use now as default
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email



class APIKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    description = models.TextField(default="API key for user endpoints")
    expires_at = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Key: {self.key[:10]}... (Expires: {self.expires_at})"


class OTP(models.Model):
    user = models.ForeignKey(Userm, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def is_expired(self):
        # OTP expires after 5 minutes (for example)
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
    
    def __str__(self):
        return f"OTP for {self.user.username}: {self.otp}"