from django.urls import path
from django.conf.urls import url

app_name = 'account'
urlpatterns = [
	path('', account.views.profileView, name='index'),
    path('entrepeneur-signup/', account.views.entSignup, name='entrepeneur-signup'),
    path('contributor-signup/', account.views.contribSignup, name='contributor-signup'),
    path('login/', account.views.signin, name='login'),
    path('logout/', account.views.signout, name='logout'),
]
