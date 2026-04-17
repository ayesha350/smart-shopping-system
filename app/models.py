from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default="Global")
    recent_searches = models.JSONField(default=list)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_data = models.JSONField()

class PriceAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=500, default="Product")
    product_id = models.CharField(max_length=255)
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_data = models.JSONField() # Reusing your existing JSON structure
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product_data.get('title')[:30]}"    