from django.urls import path
from django.conf.urls import url
from feed import views

app_name = 'feed'
urlpatterns = [
	path('', views.index, name='index'),
    path('<int:pid>/new/', views.postView, name='post'),
    path('<int:post_identifier>/delete/', views.deletePostView, name='delete'),
    path('<int:post_identifier>/edit/', views.editPostView, name='edit'),
    path('<int:pid>/follow', views.followView, name='follow'),
    path('<int:pid>/unfollow', views.unfollowView, name ='unfollow'),
    path('<str:content_type>/<int:pid>/like', views.likeView, name ='like'),
    path('<str:content_type>/<int:pid>/unlike', views.unlikeView, name ='unlike'),
    path('post/<int:post_identifier>', views.postDisplayView),
    path('search/', views.searchView, name='search'),
    path('explore/', views.searchView, name='explore'),
    path('comment/new/<int:pid>/', views.comment_on_post),
    path('comment/reply/<int:pid>/', views.comment_on_comment),
    path('comment/delete/<int:pid>', views.deleteCommentView, name='delete_comment')
    
]

#pid -> project-id
#post_identifier -> post_identifier field of post model