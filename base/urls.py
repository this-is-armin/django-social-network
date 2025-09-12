from django.urls import path
from . import views


app_name = 'base'
urlpatterns = [
    path('', views.SocialNetworkView.as_view(), name='social_network'),
]