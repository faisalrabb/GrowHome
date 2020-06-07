from django.urls import path
from django.conf.urls import url

app_name = 'account'
urlpatterns = [
	path('', account.views.profileView, name='index'),
    path('<slug:username>/', account.views.profileView, name='profile'),
    path('signup_entrepreneur/', account.views.entSignup, name='entrepeneur-signup'),
    path('signup/', account.views.contribSignup, name='contributor-signup'),
    path('login/', account.views.signin, name='login'),
    path('logout/', account.views.signout, name='logout'),
    path('update_bio/', account.views.update_bio, name='update_bio')
]
