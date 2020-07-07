from django.urls import path
from django.conf.urls import url
from account import views

app_name = 'account'
urlpatterns = [
	path('', views.profileView, name='index'),
    path('<slug:username>/', views.profileView, name='profile'),
    path('signup_entrepreneur/', views.entSignup, name='entrepeneur-signup'),
    path('signup/', views.contribSignup, name='contributor-signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('update_bio/', views.update_bio, name='update_bio'),
    path('change_password/', views.change_password, name='change_password')
]
