from django.db import models

from account.models import User
from projects.models import Project, FundingRound

# Create your models here.


class Pledge(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    funding_round = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.IntegerField()
    fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ['-created_at']


class Contribution(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    funding_round = models.ForeignKey(FundingRound, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True)
    amount_total = models.IntegerField(default=0)
    amount_after_paypal_fee = models.IntegerField(default=0)
    amount_final = models.IntegerField(default=0)
    gh_fee_amount = models.IntegerField(default=0)
    currency=models.CharField(max_length=10)
    pledge = models.ForeignKey(Pledge, on_delete=models.SET_NULL, null=True, blank=True)
    ipn_sender_email = models.EmailField(null=True, blank=True)
    paypal_invoice = models.CharField(unique=True, max_length=19)
    created_at = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ['-created_at']



class PaymentError(models.Model):
    pledge_id = models.TextField(null=True, blank=True)
    ipn_sender_email = models.EmailField(null=True, blank=True)
    paypal_invoice = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount_paid = models.IntegerField(blank=True, null=True)
    currency=models.TextField(blank=True, null=True)
    previous_contribution =models.ForeignKey(Contribution, on_delete=models.SET_NULL, blank=True, null=True)
    error_manually_handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-created_at']

class NonCompletePayment(models.Model):
    pledge_id = models.TextField(null=True, blank=True)
    ipn_sender_email = models.EmailField(null=True, blank=True)
    paypal_invoice = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    amount_paid = models.IntegerField(blank=True, null=True)
    error_manually_reviewed = models.BooleanField(default=False)
    currency=models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['-created_at']

class PaymentReversal(models.Model):
    contribution = models.ForeignKey(Contribution, on_delete=models.DO_NOTHING)
    old_amount = models.IntegerField()
    new_amount = models.IntegerField()
    change = models.IntegerField()
    description = models.TextField(blank=True, default="A payment has been reversed from PayPal, this has been recorded on the contributions page as a new negative amount contribution. No further action required unless contribution_not_found is equal to True. This should in theory never happen but if it does, contact faisal")
    created_at = models.DateTimeField(auto_now_add=True)
    contribution_not_found = models.BooleanField(default=False)

    class Meta():
        ordering = ['-created_at']

class FundingReport(models.Model):
    time= models.DateTimeField()
    text = models.TextField(blank=True, null=True)

    class Meta():
        get_latest_by ='time'
