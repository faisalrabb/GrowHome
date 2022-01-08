from projects.models import FundingRound
from contribute.models import Contribution
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Contribution)
def update_funding(sender, instance, created, **kwargs):
    if created and instance.funding_round is not None:
        instance.funding_round.total_raised = (instance.funding_round.total_raised + instance.amount)
        instance.funding_round.save()