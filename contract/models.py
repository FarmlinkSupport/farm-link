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
        ('Buyer Paid', 'Buyer Paid'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    )

    tender=models.OneToOneField(Tender,related_name='contract_tender',on_delete=models.CASCADE)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='contract_buyer')
    farmer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='contract_farmer')
    contractfileipfs=models.CharField(max_length=100,null=True)
    status=models.CharField(choices=STATUS_CHOICES,default='Active',max_length=15)
    payment_status=models.CharField(choices=PAYMENT_CHOICES,default='Pending',max_length=20)
    start_date=models.DateField(auto_now=False, auto_now_add=False)
    end_date=models.DateField(auto_now=False, auto_now_add=False)
    contract_value=models.DecimalField(max_digits=15, decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class ContractBlockchain(models.Model):
    contract=models.OneToOneField(Contract, on_delete=models.CASCADE, primary_key=True)
    blockchainaddress=models.CharField(max_length=100)

    def __str__(self):
        return str(self.contract.id)
    
class ContractDeployment(models.Model):
    contract=models.OneToOneField(Contract,on_delete=models.SET_NULL,related_name='deploy_contract')
    farmeragreed=models.BooleanField(default=False)
    buyeragreed=models.BooleanField(default=False)
    deploy_status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.contract.id)
    
class ContractDeliveryStatus(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    )

    contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
    invoice_file = models.FileField(upload_to='invoices/', null=True, blank=True) 
    buyer_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contract {self.contract.id} - Status: {self.buyer_status}"

