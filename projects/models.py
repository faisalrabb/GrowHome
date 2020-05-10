from django.db import models
from accounts.models import Country, Contributor, Entrepeneur

# Create your models here.

class Project(models.Model):
    creator = models.ForeignKey(Entrepeneur, on_delete=models.CASCADE)
    name = models.TextField(unique=True)
    problem = models.TextField()
    solution = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    city = models.CharField(max_length = 20)
    funding_round = models.ForeignKey(FundingRound, on_delete=models.SET_NULL)
    intro_video = models.FileField(upload_to='videos')
    photo = models.ImageField(upload_to='photos')

    def __str__(self):
        return self.name
    def get_absolute_url(self): 
        slug = slugify(self.name)
        return f"/projects/{slug}/"
    
class FundingRound(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    round_number = models.IntegerField()
    funding_goal = models.IntegerField()
    total_raised = models.IntegerField(default=0)
    goal_1 = models.TextField()
    goal_2 = models.TextField()
    goal_3 = models.TextField()
    info = models.TextField()
    note = models.TextField(blank=True, null=True)
    date_started = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "date_started"
        ordering = ['-round_number']


class Contribution(models.Model):
    user = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    funding_round = models.ForeignKey(Project, on_delete=models.SET_NULL)
    amount = models.IntegerField()
    
    


