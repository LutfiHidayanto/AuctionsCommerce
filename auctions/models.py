from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} {self.first_name}"
    
class Category(models.Model):
    category_name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.category_name}"
    
class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to="")
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category" )

    def __str__(self):
        return f"{self.title} {self.owner}"