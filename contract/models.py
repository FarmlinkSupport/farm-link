from django.db import models
from accounts.models import User
from tender.models import Tender


class Contract(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Terminated', 'Terminated')
    )

    PAYMENT_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    )

    tender=models.ForeignKey(Tender,on_delete=models.CASCADE,related_name='contract_tender')
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='contract_buyer')
    farmer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='contract_farmer')
    contractfileipfs=models.CharField(max_length=100,null=True)
    status=models.CharField(choices=STATUS_CHOICES,default='Active',max_length=15)
    payment_status=models.CharField(choices=PAYMENT_CHOICES,default='Pending',max_length=20)
    start_date=models.DateField(auto_now=False, auto_now_add=False)
    end_date=models.DateField(auto_now=False, auto_now_add=False)
    contract_hash=models.CharField(max_length=64)
    contract_value=models.DecimalField(max_digits=15, decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class ContractBlockchain(models.Model):
    contract=models.OneToOneField(Contract, on_delete=models.CASCADE, primary_key=True)
    blockchainaddress=models.CharField(max_length=100)
    hash_key=models.CharField(max_length=100)

    def __str__(self):
        return str(self.contract.id)
    
class ContractDeployment(models.Model):
    contract=models.OneToOneField(Contract,on_delete=models.CASCADE,related_name='deploy_contract')
    farmeragreed=models.BooleanField(default=False)
    buyeragreed=models.BooleanField(default=False)
    deploy_status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.contract.id)

