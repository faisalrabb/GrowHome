from account.models import User, Contributor, Entrepreneur
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender=User)
def delete_wrapper(sender, instance, created, **kwargs):
    try:
        uo = Entrepreneur.objects.get(user=instance)
    except:
        uo = Contributor.objects.get(user=instance)
    uo.delete()