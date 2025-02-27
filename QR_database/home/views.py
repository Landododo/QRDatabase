from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadGDSFileForm, FileFieldForm, MultipleFileField
from django.views.generic.edit import FormView
from django import forms
from .data_handlers import handle_uploaded_file, handle_sample_file
from django.db import connection
from .models import gds_files

# Create your views here.
def index(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'home.html')

def upload(request):
    if request.method == "POST":
        form = UploadGDSFileForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES["file"].name.split(".")[1] == "gds":
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/inputs/")
    else:
        form = UploadGDSFileForm()
    return render(request, "upload.html", {"form": form})

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "view.html"  # Replace with your template.
    success_url = "/view/"  # Replace with your URL or reverse().
    
    def get_context_data(self, **kwargs):
        # Get default context from parent class
        context = super().get_context_data(**kwargs)
        # Add additional data to the context
        context["file_list"] = file_list()
        context["samples"] = sample_list()
        print(context)
        return context
    
    def form_valid(self, form):
        print("doing something")
        files = tuple(self.request.FILES.getlist("file_field"))
        id = self.request.POST.get('document-select')
        print(files, id)
        for f in files:
            print(f)
            handle_sample_file(f, id)
        return super().form_valid(form)

class FileFieldFormInputs(FormView):
    form_class = FileFieldForm
    template_name = "inputs.html"  # Replace with your template.
    success_url = "/view/"  # Replace with your URL or reverse().
    
    def get_context_data(self, **kwargs):
        # Get default context from parent class
        context = super().get_context_data(**kwargs)
        # Add additional data to the context
        context["file_list"] = file_list()
        print(context)
        return context
    
    def form_valid(self, form):
        print("doing something")
        files = tuple(self.request.FILES.getlist("file_field"))
        id = self.request.POST.get('document-select')
        print(files, id)
        for f in files:
            print(f)
            handle_sample_file(f, id)
        return super().form_valid(form)
    
def file_list():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM home_gds_files")
        files = cursor.fetchall()  # Fetch all rows

    # Convert to list of dictionaries for template usage
    file_list = [
        {
            "id" : row[0],
            "file_name": row[1],
            "num_qrs": row[2],
            "qr_size": row[3],
            "qrs_per_row": row[4],
            "qrs_per_col": row[5],
            "time_uploaded": row[6],
            "last_updated": row[7],
        }
        for row in files
    ]
    return file_list

def sample_list():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM home_sample_images")
        files = cursor.fetchall()  # Fetch all rows

    # Convert to list of dictionaries for template usage
    file_list = [
        {
            "gds_file_id" : row[1],
            "file_name": row[2],
            "width": row[3],
            "height": row[4],
            "row": row[5],
            "col": row[6],
            "abs_x": row[6],
            "abs_y": row[7],
            "num_codes":row[9],
            "img_id": row[10],
        }
        for row in files
    ]
    return file_list