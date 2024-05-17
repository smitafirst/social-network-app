
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
  def create_user(self, email, username, password=None, **extra_fields):
    if not email:
      raise ValueError('The Email field must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email


class FriendRequest(models.Model):
  sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
  status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  message = models.TextField(blank=True)  # Optional message field

class Friendship(models.Model):
  user1 = models.ForeignKey(User, related_name='friendship_user1', on_delete=models.CASCADE)
  user2 = models.ForeignKey(User, related_name='friendship_user2', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

class RateLimit(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  request_count = models.IntegerField(default=0)
  last_request_time = models.DateTimeField(auto_now_add=True)
