from django.urls import path

from . import views
from .views import FileFieldFormView, FileFieldFormInputs
from .views import upload_sample_file

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("inputs/", FileFieldFormInputs.as_view(), name="inputs"),

    path("success/", views.success, name="success"),
    path("view/", FileFieldFormView.as_view(), name="view"),
    path("view_qr/<int:gds_id>/<int:row>/<int:col>/", views.view_qr_images, name="view_qr_images"),
    path('upload_sample/<int:gds_id>/<int:row>/<int:col>/', upload_sample_file, name='upload_sample_file'),

    #path("inputs/", views.inputs, name="inputs"),

]