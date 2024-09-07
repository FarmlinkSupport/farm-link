from django.db import models
from contract.models import Contract

# Create your models here.
class Payment(models.Model):
    contract=models.OneToOneField(Contract, on_delete=models.CASCADE)
    payment_date=models.DateTimeField(auto_now_add=True)
    payment_method=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return f'{self.contract.id} -> {self.id}'

