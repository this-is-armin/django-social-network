from django.urls import path
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('<pk>/', views.PostDetailView.as_view(), name='post_detail'),

    path('<pk>/like/', views.PostLikeView.as_view(), name='like'),
    path('<pk>/unlike/', views.PostUnlikeView.as_view(), name='unlike'),
]