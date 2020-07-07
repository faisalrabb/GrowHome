from django.db import models
from account.models import Entrepreneur, User, Contributor
from projects.models import Project, FundingRound, Goal
from stream_django.activity import Activity
from django_extensions.db.fields import AutoSlugField, RandomCharField

# Create your models here.

class Post(models.Model, Activity):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    funding_round=models.ForeignKey(FundingRound, on_delete=models.SET_NULL, blank=True, null=True)
    post_identifier = RandomCharField(length=10)
    title = models.CharField(max_length=250, blank=True, null=True)
    text = models.TextField()
    pfile = models.FileField(upload_to='gallery', null=True, blank=True)
    goal_accomplished = models.ForeignKey(Goal, on_delete=models.SET_NULL, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def activity_actor_attr(self):
        #activity actor is project
        return self.project
    @property
    def activity_author_feed(self):
        return "projects"
    class Meta:
        ordering = ['created_at']
    def get_absolute_url(self):
        return "/posts/%i/" % self.id
    @property
    def comments(self):
        comments = Comment.objects.filter(target=self)
        return comments
    @property
    def likes(self):
        likes = Like.objects.filter(post=self)
        return likes.count()
    @property
    def like_instances(self):
        return Like.objects.filter(post=self)
    @property
    def poster(self):
        return self.project.creator.user

class Follow(models.Model, Activity):
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('actor', 'target')
        ordering = ['-created_at']
    def activity_actor_attr(self):
        return self.actor
    @property
    def activity_notify(self):
        #notification feed goes to entrepreneur user
        return [feed_manager.get_notification_feed(self.target.creator.user.id)]

class Like(models.Model, Activity):
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    #only post or a project will be non-null value 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    project =  models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('actor', 'post', 'project')
        ordering = ['-created_at']
    def activity_actor_attr(self):
        return self.actor
    @property
    def activity_notify(self):
        #notification feed goes to entrepreneur user
        if post is not None:
            return [feed_manager.get_notification_feed(self.post.project.creator.user.id)]
        return [feed_manager.get_notification_feed(self.project.creator.user.id)]



class Comment(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    @property
    def is_project_creator(self):
        if actor == target.poster:
            return True
        else:
            return False
    
    @property
    def comment_replies(self):
        return CommentReply.objects.filter(target = self)

    def get_absolute_url(self):
        return target.get_absolute_url()
    
class CommentReply(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_project_creator(self):
        if actor == target.target.poster:
            return True
        else: 
            return False
    def get_absolute_url(self):
        return target.target.get_absolute_url()

    class Meta:
        ordering = ['created_at']


    

