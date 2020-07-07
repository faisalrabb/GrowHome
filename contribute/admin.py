from django.contrib import admin
from contribute.models import Contribution, Pledge, PaymentError, NonCompletePayment, PaymentReversal
# Register your models here.

admin.site.register(Contribution)
admin.site.register(Pledge)
#pledge should be uncommented later, only registered for testing
admin.site.register(PaymentError)
admin.site.register(NonCompletePayment)
admin.site.register(PaymentReversal)