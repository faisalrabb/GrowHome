from django.urls import path
from django.conf.urls import url

app_name = 'projects'
urlpatterns = [
	#path('', projects.views.index, name='index'),
	path('new/', projects.views.newProject, name='newProject'),
	path('<int:pid>/new/', projects.views.newFundingRound, name=''),
	path('<int:pid>/edit/', projects.views.editProject, name=''),
	path('<int:pid>/edit_fundinground/', projects.views.editProject, name=''),
    path('<slug: pslug>/', projects.views.viewProject, name=''),
	path('<int:pid>/addgoal', projects.views.addGoal, name='')
]