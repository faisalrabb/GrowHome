from feed.models import Follow, Post
from account.models import Entrepeneur, User, Contributor
from projects.models import Project
from django.db.models.signals import post_save
from django.dispatch import receiver
from stream_django.feed_manager import feed_manager

@receiver(pre_delete, sender=Follow)
def unfollow(sender, instance, using, **kwargs):
    feed_manager.unfollow_user(instance.actor.id, instance.target.id)
    instance.target.followers -= 1

@receiver(post_save, sender=Follow)
def follow(sender, instance, created, **kwargs):
    if created:
            feed_manager.follow_user(instance.actor.id, instance.target.id)
            instance.target.followers += 1
        
@receiver(post_save, sender=Like)
def like(sender, instance, created, **kwargs):
    if created:
        if instance.target_post is None:
            try:
                instance.target_project.likes += 1
            except:
                pass
        else:
            instance.target_post.likes += 1

@receiver(post_delete, sender=Like)
def unlike(sender, instance, created, **kwargs):
    if created:
        if instance.target_post is None:
            try:
                instance.target_project.likes -= 1
            except:
                pass
        else:
            instance.target_post.likes -= 1

@receiver(pre_save, sender=Post)
def uncheck_goals(sender, instance, created, **kwargs):
    goal = instance.goal_accomplished
    if goal is not None:
        instance.goal_accomplished.accomplished = False
        instance.goal_accomplished.save()

@receiver(post_save, sender=Post)
def uncheck_goals(sender, instance, created, **kwargs):
    goal = instance.goal_accomplished
    if goal is not None:
        instance.goal_accomplished.accomplished = True
        instance.goal_accomplished.save()





