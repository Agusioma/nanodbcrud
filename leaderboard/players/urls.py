from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add_player, name="add_player"),
    path("update/", views.update_score, name="update_score"),
    path("delete/", views.delete_player, name="delete_player"),
]
