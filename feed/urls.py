from django.urls import path
from django.conf.urls import url

app_name = 'feed'
urlpatterns = [
	path('', feed.views.index, name='index'),
    path('new/<int:pid>/', feed.views.postView, name='post'),
    path('follow/<str:fusername>/', feeds.views.followView, name='follow'),
    path('unfollow/<str:fusername>/', feeds.views.unfollowView, name ='unfollow')
    path('delete/<int:post_identifier>/', feeds.views.deletePostView, name='delete'),
    path('edit/<int:post_identifier>/', feeds.views.editPostView, name='edit'),
    #the rest of the url patterns are search
    path('search/', feeds.views.searchView, name='search'),
    path('explore/', feeds.views.searchView, name='explore'),
    path('explore/<int:page_number>/', feeds.views.searchView),
    path('search/<int:page_number>/', feeds.views.searchView),
    path('search/<str:query>/', feeds.views.searchView),
    path('search/<str:country_name>/', feeds.views.searchView),
    path('search/<str:query>/<int:page_number>/', feeds.views.searchView),
    path('search/<str:query>/<str: country_name>/<int:page_number>/', feeds.views.searchView),
    path('search/<str:query>/<str:country_name>/', feeds.views.searchView),
    path('search/<str:country_name>/<int:page_number>/', feeds.views.searchView),
]

#pid -> project-id
#post_identifier -> post_identifier field of post model