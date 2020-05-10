from django.db import models
from accounts.models import Entrepeneur, User, Contributor
from projects.models import Project
from stream_django.activity import Activity

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
        #notification feed goes to entrepeneur
        return [feed_manager.get_notification_feed(self.target.creator.id)]

class Post(models.Model, activity.Activity):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField()
    pfile = models.FileField(upload_to='gallery', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def activity_actor_attr(self):
        #activity by project, not entrepeneur
        return self.project
        

