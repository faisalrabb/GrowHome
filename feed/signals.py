from feed.models import Follow, Post
from account.models import Entrepeneur, User, Contributor
from projects.models import Project
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_delete, sender=Follow)
def unfollow(sender, instance, created, **kwargs):
    feed_manager.unfollow_user(instance.actor.id, instance.target.id)

@receiver(post_delete, sender=Follow)
def follow(sender, instance, created, **kwargs):
    if created:
            feed_manager.follow_user(instance.actor.id, instance.target.id)
        

@receiver(post_save, sender=Contributor)
def followlocal(sender, instance, created, **kwargs):
    if created:
        country = instance.country
        #implement