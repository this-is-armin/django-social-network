from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('signin/', views.UserSignInView.as_view(), name='signin'),
    path('signout/', views.UserSignOutView.as_view(), name='signout'),

    path('profile/<username>/', views.UserProfileView.as_view(), name='profile'),
    path('delete/<username>/', views.UserDeleteView.as_view(), name='delete-account'),
    path('edit/<username>/', views.UserEditView.as_view(), name='edit-account'),
    
    path('follow/<username>/', views.UserFollowView.as_view(), name='follow'),
    path('unfollow/<username>/', views.UserUnfollowView.as_view(), name='unfollow'),
    path('followers/<username>/', views.UserFollowersView.as_view(), name='followers'),
    path('following/<username>/', views.UserFollowingView.as_view(), name='following'),
    
    path('posts/<username>/', views.UserPostsView.as_view(), name='posts'),
    path('comments/<username>/', views.UserCommentsView.as_view(), name='comments'),
    path('saved-posts/<username>/', views.UserSavedPostsView.as_view(), name='saved-posts'),
    path('liked-posts/<username>/', views.UserLikedPostsView.as_view(), name='liked-posts'),
]