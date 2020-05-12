from django.db import models
from accounts.models import Country, Contributor, Entrepeneur
from stream_django.activity import Activity

# Create your models here.

class Project(models.Model):
    creator = models.ForeignKey(Entrepeneur, on_delete=models.CASCADE)
    name = models.TextField(unique=True)
    problem = models.TextField()
    solution = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    city = models.CharField(max_length = 20)
    intro_video = models.FileField(upload_to='videos')
    photo = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.name
    def get_absolute_url(self): 
        slug = slugify(self.name)
        return reverse('view', kwargs={'pid' = self.pk})
    class Meta:
        get_latest_by = "date_started"
        ordering = ['-round_number']
    
class FundingRound(models.Model, activity.Activity):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    round_number = models.IntegerField(default = 1)
    funding_goal = models.IntegerField()
    total_raised = models.IntegerField(default=0)
    goal_1 = models.TextField()
    goal_1_finished = models.BooleanField(default=False)
    goal_2 = models.TextField()
    goal_2_finished = models.BooleanField(default=False)
    goal_3 = models.TextField()
    goal_3_finished = models.BooleanField(default=False)
    info = models.TextField()
    video = models.FileField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date_started = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "date_started"
        ordering = ['-round_number']
    def activity_actor_attr(self):
        return self.project


class Contribution(models.Model, activity.Activity):
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    funding_round = models.ForeignKey(Project, on_delete=models.SET_NULL)
    amount = models.IntegerField()
    



