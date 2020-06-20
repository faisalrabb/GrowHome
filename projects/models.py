from django.db import models
from accounts.models import Country, Contributor, Entrepeneur
from stream_django.activity import Activity
from django_extensions.db.fields import AutoSlugField

# Create your models here.

class Project(models.Model, activity.Activity):
    creator = models.ForeignKey(Entrepeneur, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=80)
    problem = models.TextField()
    solution = models.TextField()
    category= models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    info = models.TextField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL)
    city = models.CharField(max_length = 20)
    intro_video = models.FileField(upload_to='videos')
    photo = models.ImageField(upload_to='photos')
    looking_for= models.ManyToManyField(Collaborator, null=True, blank=True)
    #automated fieds
    slug = AutoSlugField(populate_from='name')
    seeking_funding = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def activity_actor_attr(self):
        return creator.user
    def __str__(self):
        return self.name
    def get_absolute_url(self): 
        return reverse(projects.views.viewProject, kwargs={'pid':self.id})
    class Meta:
        get_latest_by = "created_at"
        ordering = ['-created_at']
    @property
    def like_instances(self):
        return Like.objects.filter(project=self)
    @property
    def likes(self):
        likes = Like.objects.filter(project=self)
        return likes.count()
    @property
    def followers(self):
        follows = Follow.objects.filter(project=self)
        return follows.count()
    @property
    def followers_instances (self):
        follows = Follow.objects.filter(project=self)
        return follows
    
class FundingRound(models.Model, activity.Activity):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    round_number = models.IntegerField(default = 1)
    funding_goal = models.IntegerField()
    total_raised = models.IntegerField(default=0)
    info = models.TextField()
    video = models.FileField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    #automated fields
    created_at = models.DateField(auto_now_add=True)
    goals_finished = models.BooleanField(default=False)
    funding_finished = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "created_at"
        ordering = ['-round_number']
        unique_together = ['round_number', 'project']
    @property
    def activity_actor_attr(self):
        return self.project
    @property
    def activity_author_feed(self):
        return "projects"
    @property
    def goals(self):
        return Goal.objects.filter(funding_round=self)

    def __str__(self):
        pr = self.project.__str__()
        final = pr + str(self.round_number)
        return final

class Category(models.Mode):
    title = models.TextField()

    def __str__(self):
        return self.title

class Collaborator(models.Model):
    function = models.CharField(max_length=32)

    def __str__(self):
        return self.function

class Goal(models.Model):
    text = models.TextField()
    accomplished = models.BooleanField(default=False)
    funding_round = models.ForeignKey(FundingRound, on_delete=models.CASCADE)

    def __str__(self):
        return self.text + ": " + funding_round.__str__()

#class ErrorReport(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.SET_NULL)
#    source = models.TextField()
 #   object_data = models.TextField()





