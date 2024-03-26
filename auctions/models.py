from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db.models.functions import Cast

class User(AbstractUser):
    def __str__(self):
        return f"{self.username} {self.first_name}"
    
class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"
    
class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to="")
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True, related_name="owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    def date_validator(value):
        if value < timezone.now():
            raise("Date cannot be in the past")
        
    start_date = models.DateTimeField(validators=[date_validator], null=True)
    end_date = models.DateTimeField(validators=[date_validator], null=True)

    def is_active(self):
        return self.end_date > timezone.now()
    
    def __str__(self):
        return f"{self.title} {self.owner}"     
    
class Bid(models.Model):
    amount = models.DecimalField(decimal_places = 2, max_digits=7)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")

    def __str__(self):
        return f"{self.user} {self.listing} {self.amount}"
    
