from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Recipe(models.Model):
    title =models.CharField(max_length=200,blank=False)
    description = models.TextField(blank=True,null=True)
    ingredients = models.TextField(blank=False,null=False)
    instructions = models.TextField(blank=False)
    image=models.ImageField(upload_to='images',blank=True,null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    created_by =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="recipes")

    def __str__(self):
        return self.title
    
class UserProfile(AbstractUser):
    ROLE_CHOICE=(
        ("admin","Admin"),
        ("user","User"),
    )
    
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    role = models.CharField(max_length=5,choices=ROLE_CHOICE, null=True, blank=True)    
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username



    