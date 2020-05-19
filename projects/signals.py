from projects.models import FundingRound
from contribute.models import Contribution
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Contribution)
def update_funding(sender, instance, created, **kwargs):
    if created:
        instance.funding_round.total_raised = (instance.funding_round.total_raised + instane.amount)
        instance.funding_round.save()
        #send e-mail to sender

@receiver(post_save, sender=FundingRound)
def mark_complete(sender, instance, created, **kwargs):
    if not created:
        if instance.goal_1_finished and instance.goal_2_finished and instance.goal_3_finished and not instance.is_completed:
            instance.is_completed = True
            instance.save()
