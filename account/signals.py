from account.models import User, Contributor, Entrepeneur, Country
from project.models import Project
from django.db.models.signals import post_save
from django.dispatch import receiver
from stream_django.feed_manager import feed_manager


@receiver(post_save, sender=Entrepeneur)
@receiver(post_save, sender=Contributor)
def follow_local(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        country = instance.country
        curated_projects = Projects.objects.filter(country=country, featured=True)[:10]
        for project in curated_projects:
            follow = Follow(
                actor = user,
                target = project
            )
            follow.save()
            feed_manager.follow_user(user.id, project.id)