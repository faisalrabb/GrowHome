from projects.models import FundingRound
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=FundingRound)
def mark_complete(sender, instance, created, **kwargs):
    if not created:
        if instance.goal_1_finished and instance.goal_2_finished and instance.goal_3_finished and not instance.goals_finished:
            instance.goals_finished = True
        if instance.funding_goal <= instance.total_raised and not instance.funding_finished:
            instance.funding_finished = True
        if instance.funding_finished:
            funding_rounds = FundingRound.objects.filter(project = instance.project)
            instance.project.seeking_funding = False
            for funding_round in funding_rounds:
                if not funding_round.funding_finished:
                    instance.project.seeking_funding = True
            instance.project.save()
        instance.save()
