from django.urls import path
from django.conf.urls import url
from projects import views

app_name = 'projects'
urlpatterns = [
	#path('', views.index, name='index'),
	path('new/', views.newProject, name='new_project'),
	path('delete/<int:pid>/', views.deleteProject, name='delete_project'),
	path('<int:pid>/new/', views.newFundingRound, name='new_funding_round'),
	path('<int:pid>/edit/', views.editProject, name='edit_project'),
	path('<int:pid>/edit_fundinground/', views.editFundingRound, name='edit_funding_round'),
    path('<slug: pslug>/', views.viewProject, name='view_project'),
	path('<int:pid>/addgoal', views.addGoal, name='add_goal')
]