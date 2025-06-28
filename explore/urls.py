from django.urls import path
from . import views


app_name = 'explore'
urlpatterns = [
    path('', views.ExploreView.as_view(), name='explore'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('<int:pk>/comment-delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('new-post/', views.NewPostView.as_view(), name='new-post'),
    path('<int:pk>/edit/', views.PostEditView.as_view(), name='post-edit'),
    path('<int:pk>/save/', views.PostSaveView.as_view(), name='post-save'),
    path('<int:pk>/unsave/', views.PostUnSaveView.as_view(), name='post-unsave'),
    path('<int:pk>/like/', views.PostLikeView.as_view(), name='post-like'),
    path('<int:pk>/unlike/', views.PostUnLikeView.as_view(), name='post-unlike'),
]