from feed.models import Follow, Post
from account.models import Entrepeneur, User, Contributor
from projects.models import Project
from django.db.models.signals import post_save
from django.dispatch import receiver
from stream_django.feed_manager import feed_manager

@receiver(pre_delete, sender=Follow)
def unfollow(sender, instance, using, **kwargs):
    #unfollow project feed
    news_feeds = feed_manager.get_news_feeds(instance.actor.id)
    target_feed = feed_manager.get_feed('projects', instance.target.id) #get custom feed
    for feed in news_feeds.values():
        feed.unfollow(target_feed.slug, target_feed.user_id)

@receiver(post_save, sender=Follow)
def follow(sender, instance, created, **kwargs):
    if created:
            #follow project feed
            news_feeds = feed_manager.get_news_feeds(instance.actor.id)
            target_feed = feed_manager.get_feed('projects', instance.target.id) #get custom feed
            for feed in news_feeds.values():
                feed.follow(target_feed.slug, target_feed.user_id)
        
#@receiver(post_save, sender=Like)
#def like(sender, instance, created, **kwargs):
#    if created:
#        if instance.target_post is None:
#            try:
#                instance.target_project.likes += 1
#            except:
#                pass
#        else:
#            instance.target_post.likes += 1

#@receiver(post_delete, sender=Like)
#def unlike(sender, instance, created, **kwargs):
#    if created:
#        if instance.target_post is None:
#            try:
#                instance.target_project.likes -= 1
#            except:
#                pass
#        else:
#            instance.target_post.likes -= 1

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

@receiver(post_save, sender=Project)
def follow_own(sender, instance, created, **kwargs):
    if created:
        user = instance.creator.user
        follow = Follow(actor=user, target=instance)
        follow.save()

@receiver(post_save, sender=Entrepeneur)
@receiver(post_save, sender=Contributor)
def follow_local(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        country = instance.country
        if country is not None:
            curated_projects = Projects.objects.filter(country=country, featured=True)[:10]
        else:
            curated_projects = Projects.objects.filter(featured=True)[:10]
        for project in curated_projects:
            follow = Follow(
                actor = user,
                target = project
            )
            follow.save()
            feed_manager.follow_user(user.id, project.id)







