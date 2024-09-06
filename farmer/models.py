from django.db import models
from accounts.models import User

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    farm_name = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"Farmer: {self.user.name} - {self.farm_name}"