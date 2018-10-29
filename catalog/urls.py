from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "catalog"

urlpatterns = [
    path('', views.index, name='index'),
]