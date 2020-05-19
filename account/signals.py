from account.models import User, Contributor, Entrepeneur
from project.models import Project, CuratedProject
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from stream_django.feed_manager import feed_manager



@receiver(post_save, sender=Entrepeneur)
@receiver(post_save, sender=Contributor)
def follow_local(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        country = instance.country
        curated_projects = CuratedProject.objects.filter(country=country)[:10]
        for curated_project in curated_projects:
            feed_manager.follow_user(instance.user.id, curated_project.project.id)