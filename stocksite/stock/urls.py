from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("Graph/", views.Graph, name="Graph"),
    path("Canvas/", views.Canvas, name="Canvas"),
]