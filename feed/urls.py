from django.urls import path
from django.conf.urls import url

app_name = 'feed'
urlpatterns = [
	path('', feed.views.index, name='index'),
    path('new/<int:pid>/', feed.views.postView, name='post'),
    path('delete/<int:post_identifier>/', feeds.views.deletePostView, name='delete'),
    path('edit/<int:post_identifier>/', feeds.views.editPostView, name='edit'),
    path('follow/<int:pid>/', feeds.views.followView, name='follow'),
    path('unfollow/<int:pid>/', feeds.views.unfollowView, name ='unfollow')
    path('posts/<int:pid>', feeds.views.postDisplayView)
    path('search/', feeds.views.searchView, name='search'),
    path('explore/', feeds.views.searchView, name='explore'),
    path('comment/new/<int:pid>/', feeds.views.comment_on_post),
    path('comment/reply/<int:pid>/', feeds.views.comment_on_comment),
    
]

#pid -> project-id
#post_identifier -> post_identifier field of post model