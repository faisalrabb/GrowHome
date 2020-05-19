from feed.models import Follow, Post
from account.models import Entrepeneur, User, Contributor
from projects.models import Project
from django.db.models.signals import post_save
from django.dispatch import receiver
from stream_django.feed_manager import feed_manager

@receiver(pre_delete, sender=Follow)
def unfollow(sender, instance, using, **kwargs):
    feed_manager.unfollow_user(instance.actor.id, instance.target.id)

@receiver(post_save, sender=Follow)
def follow(sender, instance, created, **kwargs):
    if created:
            feed_manager.follow_user(instance.actor.id, instance.target.id)
        

#this should be in account app.
@receiver(post_save, sender=Entrepeneur)
@receiver(post_save, sender=Contributor)
def follow_local(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        country = instance.country
        curated_projects = CuratedProjects.objects.filter(country=country)[:10]
        for project in curated_projects:
            feed_manager.follow_user(instance.user.id, project.id)





