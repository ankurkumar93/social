from django.contrib import admin
from django.urls import path
from .views import UserLoginView, GetUserView, FollowUserView, UnFollowUserView, PostView, LikePostView, CommentPostView, GetPostView, AllPostView
urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('user', GetUserView.as_view(), name='user'),
    path('follow/<str:id>', FollowUserView.as_view(), name='follow'),
    path('unfollow/<str:id>', UnFollowUserView.as_view(), name='unfollow'),
    path('getuser/<str:id>', GetUserView.as_view(), name='getuser'),
    path('post/', PostView.as_view(), name='post'),
    path('post/<str:id>', PostView.as_view(), name='post'),
    path('likepost/<str:id>', LikePostView.as_view(), name='likepost'),
    path('commentpost/<str:id>', CommentPostView.as_view(), name='commentpost'),
    path('getpost/<str:id>', GetPostView.as_view(), name='getpost'),
    path('allpost/', AllPostView.as_view(), name='allpost'),
]