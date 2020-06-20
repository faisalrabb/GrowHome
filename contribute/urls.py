from django.urls import path
from django.conf.urls import url

app_name = 'contribute'
urlpatterns = [
    path('', contribute.views.index, name='index'),
    path('edit/, contribute.views.edit_pledge', name='edit')
    path('done/', contribute.views.done, name='done'),
    path('canceled/', contribute.views.canceled, name='canceled'),
]