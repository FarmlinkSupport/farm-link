from django.db import models
from accounts.models import User

class Tender(models.Model):
    STATUS_CHOICES = (
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Awarded', 'Awarded')
    )

    title = models.CharField(max_length=250)
    company_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='tender_buyer')
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    minimum_bid = models.DecimalField(max_digits=15, decimal_places=2)
    maximum_bid = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=200,null=True, blank=True)
    notice_file = models.FileField(upload_to="tender/", max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.title[:30]}'

