from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid

class UserManager(BaseUserManager):
    def create_user(self, wallet_address):
        if not wallet_address:
            raise ValueError("Users must have a wallet address")
        
        user = self.model(
            wallet_address=wallet_address,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, wallet_address, **extra_fields):
        user = self.create_user(
            wallet_address=wallet_address,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_address = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    twitter_handle = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'wallet_address'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username or self.wallet_address

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def total_events_organized(self):
        return self.organized_events.count()

    @property
    def total_tickets_sold(self):
        return sum(event.tickets_sold for event in self.organized_events.all())

    @property
    def total_revenue(self):
        return sum(event.revenue for event in self.organized_events.all())
