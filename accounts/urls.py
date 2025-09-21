from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.PeopleView.as_view(), name='people'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path('<username>/', views.ProfileView.as_view(), name='profile'),

    path('<username>/edit/', views.AccountEditView.as_view(), name='edit_account'),
    path('<username>/delete-profile-image/', views.ProfileImageDeleteView.as_view(), name='delete_profile_image'),
    path('<username>/delete/', views.AccountDeleteView.as_view(), name='delete_account'),

    path('<username>/follow/', views.FollowView.as_view(), name='follow'),
    path('<username>/unfollow/', views.UnfollowView.as_view(), name='unfollow'),

    path('<username>/followers/', views.FollowersView.as_view(), name='followers'),
    path('<username>/following/', views.FollowingView.as_view(), name='following'),

    path('<username>/posts/', views.PostsView.as_view(), name='posts'),

    path('<username>/create-post/', views.PostCreateView.as_view(), name='create_post'),
    path('<username>/posts/<pk>/edit/', views.PostEditView.as_view(), name='edit_post'),
    path('<username>/posts/<pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
]