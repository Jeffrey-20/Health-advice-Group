

from django.urls import path
from . import views

urlpatterns = [
    # ... your other paths ...
    path('', views.home, name='home'),
    path('forecast/', views.forecast, name='forecast'),
    path('dashboard', views.dashboard_view,name='dashboard' ),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),

    path('delete-log/<int:pk>/', views.delete_impact, name='delete_impact'),
    path('download-logs/', views.download_impacts, name='download_impacts'),

]