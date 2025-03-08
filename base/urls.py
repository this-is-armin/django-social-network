from django.urls import path

from . import views


app_name = 'base'
urlpatterns = [
    path('', views.home_view, name='home'),

    path('posts/', views.PostsView.as_view(), name='posts'),
    path('post-create/', views.PostCreateView.as_view(), name='post_create'),

    path('posts/<pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<pk>/delete/', views.post_delete_view, name='post_delete'),
    path('posts/<pk>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('posts/<pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<pk>/save/', views.PostSaveView.as_view(), name='post_save'),
    path('posts/<pk>/un-save/', views.PostUnSaveView.as_view(), name='post_un_save'),
    path('posts/<pk>/<comment_pk>/', views.post_comment_delete, name='post_comment_delete'),
]
