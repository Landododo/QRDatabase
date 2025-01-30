from django.urls import path

from . import views
from .views import FileFieldFormView

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("inputs/", FileFieldFormView.as_view(), name="inputs"),

    path("success/", views.success, name="success"),
    path("view/", views.view, name="view"),
    #path("inputs/", views.inputs, name="inputs"),



]