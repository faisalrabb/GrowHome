from django.urls import path
from django.conf.urls import url

app_name = 'feed'
urlpatterns = [
	path('', feed.views.index, name='index'),
    path('<int:pid>/new/', feed.views.postView, name='post'),
    path('<int:post_identifier>/delete/', feeds.views.deletePostView, name='delete'),
    path('<int:post_identifier>/edit/', feeds.views.editPostView, name='edit'),
    path('<int:pid>/follow', feeds.views.followView, name='follow'),
    path('<int:pid>/unfollow', feeds.views.unfollowView, name ='unfollow'),
    path('<str:content_type>/<int:pid>/like', feeds.views.likeView, name ='like'),
    path('<str:content_type>/<int:pid>/unlike', feeds.views.unlikeView, name ='unlike'),
    path('post/<int:post_identifier>', feeds.views.postDisplayView)
    path('search/', feeds.views.searchView, name='search'),
    path('explore/', feeds.views.searchView, name='explore'),
    path('comment/new/<int:pid>/', feeds.views.comment_on_post),
    path('comment/reply/<int:pid>/', feeds.views.comment_on_comment),
    path('comment/delete/<int:pid>', feeds.views.deleteCommentView, name='delete_comment')
    
]

#pid -> project-id
#post_identifier -> post_identifier field of post model