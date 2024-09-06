from django.db import models
from accounts.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=50)
    company_address = models.CharField(max_length=100)
    company_zipcode = models.CharField(max_length=6)
    gst_no = models.CharField(max_length=15)
    is_verified=models.BooleanField(default=False)

    def __str__(self):
        return self.user.name
