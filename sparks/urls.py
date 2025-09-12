from django.urls import path
from . import views


app_name = 'sparks'
urlpatterns = [
    path('', views.SparksView.as_view(), name='sparks'),
    path('<pk>/', views.SparkDetailView.as_view(), name='spark_detail'),
    path('<pk>/edit/', views.EditSparkView.as_view(), name='edit_spark'),
    path('<pk>/delete/', views.DeleteSparkView.as_view(), name='delete_spark'),
]