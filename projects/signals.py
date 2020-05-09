from projects.models import Contribution, FundingRound
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Contribution)
def update_funding(sender, instance, created, **kwargs):
    if created:
        instance.funding_round.total_raised = (instance.funding_round.total_raised + instane.amount)
        instance.funding_round.save()

