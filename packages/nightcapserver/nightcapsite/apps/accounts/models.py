from django.db import models
from django.contrib.auth.models import User
from django.utils import tree
from django.utils.regex_helper import normalize

# Create your models here.
class UserInterest(models.Model):
    name = models.CharField(max_length=64, unique=True)
    normalized_name = models.CharField(max_length=64, unique=True)

    def  __str__(self):
        return self.name

class UserPersona(models.Model):
    name = models.CharField(max_length=64, unique=True)
    normalized_name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    # owner
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    # settings
    is_full_name_displayed = models.BooleanField(default=True)

    # details
    name = models.CharField(max_length=40, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    
    persona = models.ForeignKey(UserPersona, on_delete=models.SET_NULL, blank=True, null=True)
    interests = models.ManyToManyField(UserInterest, blank=True)

