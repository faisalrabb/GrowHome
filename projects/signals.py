from projects.models import FundingRound
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Goal)
def mark_complete(sender, instance, created, **kwargs):
    if created:
        if instance.funding_round.goals_finished == True:
            instance.funding_round.goals_finished = False
            instance.funding_round.save()
    else:
        if instance.accomplished == True:
            goals = Goal.objects.filter(funding_round=instance.funding_round)
            unaccomplished_goals = 0
            for goal in goals:
                if not goal.accomplished:
                    unaccomplished += 1
                    instance.funding_round.goals_finished=False
            if unaccomplished_goals != 0 and instance.funding_round.goals_finished == True:
                instance.funding_round.goals_finished=False
                instance.funding_round.save()
            elif unaccomplished_goals == 0 and instance.funding_round.goals_finished == False:
                instance.funding_round.goals_finished=True
                instance.funding_round.save()
        elif instance.accomplished == False:
            if instance.funding_round.goals_finished==True:
                instance.funding_round.goals_finished==False
                instance.funding_round.save()

@receiver(post_save, sender=FundingRound)
def set_seeking_funding(sender, instance, created, **kwargs):
    if created:
        if instance.project.seeking_funding==False:
            instnace.project.seeking_funding=True
            instance.project.save()
    else:
        if instance.total_raised >= instance.funding_goal and instance.funding_finished == False:
            instance.funding_finished = True
            instance.save()
            fundingrounds = FundingRound.objects.filter(project=instance.project)
            seeking = 0
            for fundinground in fundingrounds:
                if !fundinground.funding_finished:
                    seeking += 1
            if seeking != 0 and instance.project.seeking_funding == False:
                instance.project.seeking_funding = True
                instance.project.save()
            elif seeking == 0 and instance.project.seeking_funding == True:
                instance.project.seeking_funding = False
                instance.project.save()