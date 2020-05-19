from django.db import models
from accounts.models import Entrepeneur, User, Contributor
from projects.models import Project
from stream_django.activity import Activity
from django_extensions.db.fields import AutoSlugField, RandomCharField

# Create your models here.


class Follow(models.Model, activity.Activity):
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('actor', 'target')
    def activity_actor_attr(self):
        return self.actor
    @property
    def activity_notify(self):
        #notification feed goes to entrepeneur user
        return [feed_manager.get_notification_feed(self.target.creator.user.id)]

class Post(models.Model, activity.Activity):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    funding_round=models.ForeignKey(FundingRound, on_delete=models.SET_NULL)
    post_identifier = RandomCharField(max_length=10)
    title = models.CharField(max_length=250, blank=True, null=True)
    text = models.TextField()
    pfile = models.FileField(upload_to='gallery', null=True, blank=True)
    goal_accomplished = models.BooleanField()
    goal_text= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def activity_actor_attr(self):
        #activity actor is project
        return self.project


