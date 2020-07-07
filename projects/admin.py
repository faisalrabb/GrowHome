from django.contrib import admin
from projects.models import Project, FundingRound, Category, Collaborator, Goal

# Register your models here.

admin.site.register(Project)
admin.site.register(FundingRound)
admin.site.register(Category)
admin.site.register(Collaborator)
admin.site.register(Goal)
#comment goal later, its registered only for testing purposes