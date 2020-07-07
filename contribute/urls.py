from django.urls import path
from django.conf.urls import url
from contribute import views

app_name = 'contribute'
urlpatterns = [
    path('', views.index, name='index'),
    #path('edit/', views.edit_pledge, name='edit'),
    path('done/', views.done, name='done'),
    path('canceled/', views.canceled, name='canceled'),
]