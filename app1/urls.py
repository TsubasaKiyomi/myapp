
from django.urls import path
from . import views

urlpatterns = [
    path("", views.aisatsu, name="aisatsu"),
]
