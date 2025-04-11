"""
URL configuration for QR_database project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path("", include("home.urls")),
    path('admin/', admin.site.urls),
    # path("api/files/", views.api_file_list, name="api-files"),
    # path("api/samples/", views.api_sample_list, name="api-samples"),
    path("view_qr/<int:gds_id>/<int:row>/<int:col>/", views.view_qr_images, name="view_qr_images"),
    path("view/<int:gds_file_id>/", views.FileFieldFormView.as_view(), name="view"),



]
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)