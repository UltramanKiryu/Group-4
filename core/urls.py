from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('comment-post', views.comment_post, name='comment-post'),
    path('listss', views.listss, name='listss'),
    path('events', views.events, name='events'),
    path('delete', views.delete, name='delete'),
    path('edit', views.edit, name='edit'),
    path('share', views.share, name='share'),
    path('friends', views.friends, name='friends'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
]
