from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class User(AbstractUser):
    #avatar = models.ImageField()
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=1000,blank=True)

    is_public = models.BooleanField(default=True)

    
