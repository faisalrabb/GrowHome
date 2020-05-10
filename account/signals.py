from account.models import User, Contributor, Entrepeneur
from django.db.models.signals import post_save
from django.dispatch import receiver

#
#@receiver(post_delete, sender=User)
#def delete_wrapper(sender, instance, created, **kwargs):
#    try: 
#        wrapper = Entrepeneur.objects.get(user=instance)
#    except: 
#        wrapper = Contributor.objects.get(user=instance)
#    wrapper.delete()



