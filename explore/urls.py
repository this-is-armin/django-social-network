from django.urls import path
from . import views


app_name = 'explore'
urlpatterns = [
    path('', views.ExploreView.as_view(), name='explore'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete-post'),
    path('<int:pk>/delete-comment/', views.CommentDeleteView.as_view(), name='delete-comment'),
    path('new-post/', views.NewPostView.as_view(), name='new-post'),
    path('<int:pk>/edit/', views.EditPostView.as_view(), name='edit-post'),
]