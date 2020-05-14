from django.db import models
from accounts.models import Country, Contributor, Entrepeneur
from stream_django.activity import Activity
from django_extensions.db.fields import AutoSlugField

# Create your models here.

class Project(models.Model):
    creator = models.ForeignKey(Entrepeneur, on_delete=models.CASCADE)
    name = models.TextField(unique=True)
    slug = AutoSlugField(populate_from='name')
    problem = models.TextField()
    solution = models.TextField()
    category= models.ForeignKey(Category, on_delete=models.SET_NULL)
    info = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    city = models.CharField(max_length = 20)
    intro_video = models.FileField(upload_to='videos')
    photo = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.name
    def get_absolute_url(self): 
        return reverse(projects.views.viewProject, args=[slug]) #<- possible error in reverse
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
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "date_started"
        ordering = ['-round_number']
    def activity_actor_attr(self):
        return self.project.creator


class Contribution(models.Model):
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    funding_round = models.ForeignKey(Project, on_delete=models.SET_NULL)
    amount = models.IntegerField()

class Category(models.Mode):
    title = models.TextField()

    def __str__(self):
        return self.title

#class ErrorReport(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.SET_NULL)
#    source = models.TextField()
 #   object_data = models.TextField()





