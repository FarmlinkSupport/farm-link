from django.contrib import admin
from .models import Contract,ContractDeployment,ContractBlockchain,ContractDeliveryStatus

# Register your models here.
admin.site.register(Contract)
admin.site.register(ContractDeployment)
admin.site.register(ContractBlockchain)
admin.site.register(ContractDeliveryStatus)
