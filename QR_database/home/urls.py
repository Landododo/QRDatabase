from django.urls import path

from . import views
from .views import FileFieldFormView, FileFieldFormInputs

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("inputs/", FileFieldFormInputs.as_view(), name="inputs"),

    path("success/", views.success, name="success"),
    path("view/", FileFieldFormView.as_view(), name="view"),
    #path("inputs/", views.inputs, name="inputs"),



]