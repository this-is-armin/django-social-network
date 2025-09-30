from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),

    path('create-post/', views.PostCreateView.as_view(), name='create_post'),

    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/edit/', views.PostEditView.as_view(), name='edit_post'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('<int:pk>/like/', views.PostLikeView.as_view(), name='like'),
    path('<int:pk>/unlike/', views.PostUnlikeView.as_view(), name='unlike'),
]