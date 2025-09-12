from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('', views.PeopleView.as_view(), name='people'),
    
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('<username>/', views.ProfileView.as_view(), name='profile'),
    path('<username>/edit/', views.EditAccountView.as_view(), name='edit_account'),
    path('<username>/delete-profile-image/', views.DeleteProfileImageView.as_view(), name='delete_profile_image'),
    path('<username>/delete/', views.DeleteAccountView.as_view(), name='delete_account'),

    path('<username>/add-spark/', views.AddSparkView.as_view(), name='add_spark'),
    path('<username>/sparks/', views.SparksView.as_view(), name='sparks'),

    path('<username>/follow/', views.FollowView.as_view(), name='follow'),
    path('<username>/unfollow/', views.UnfollowView.as_view(), name='unfollow'),

    path('<username>/followers/', views.FollowersListView.as_view(), name='followers_list'),
    path('<username>/following/', views.FollowingListView.as_view(), name='following_list'),
]