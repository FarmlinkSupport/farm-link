from django.db import models
from accounts.models import User
from tender.models import Tender

# Create your models here.
class Draft(models.Model):
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending')
    )

    farmer=models.ForeignKey(User, on_delete=models.CASCADE,related_name='draft_farmer')
    tender=models.ForeignKey(Tender, on_delete=models.CASCADE,related_name='tender_draft')
    draftfile=models.FileField(upload_to='draft/', max_length=150)
    status=models.CharField(choices=STATUS_CHOICES,default='Pending',max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.farmer.id} -> {self.tender.id}'

