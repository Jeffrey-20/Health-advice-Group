

from django.urls import path
from . import views

urlpatterns = [
    # ... your other paths ...
    path('', views.home, name='home'),
    path('forecast/', views.forecast, name='forecast'),
]