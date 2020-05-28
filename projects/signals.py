from projects.models import FundingRound
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Goal)
def mark_complete(sender, instance, created, **kwargs):
    if not created:
        if instance.accomplished == True:
            goals = Goal.objects.filter(funding_round=instance.funding_round)
            instance.funding_round.goals_finished = True
            for goal in goals:
                if not goal.accomplished:
                    instance.funding_round.goals_finished=False
            instance.funding_round.save()
        elif instance.accomplished == False:
            if instance.funding_round.goals_finished==True:
                instance.funding_round.goals_finished==False
