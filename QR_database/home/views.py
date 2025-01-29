from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadGDSFileForm, FileFieldForm, MultipleFileField
from django.views.generic.edit import FormView
from django import forms
from .data_handlers import handle_uploaded_file, handle_uploaded_files


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

def inputs(request):
    if request.method == "POST":
        form = MultipleFileField(request.POST, request.FILES)
        if form.is_valid() and request.FILES["file"].name.split(".")[1] == "gds":
            handle_uploaded_files(request.FILES["file"])
            return HttpResponseRedirect("/view/")
    else:
        form = UploadGDSFileForm()
    return render(request, "inputs.html", {"form": form})

def view(request):
    if request.method == "POST":
        form = UploadGDSFileForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES["file"].name.split(".")[1] == "gds":
            handle_uploaded_file(request.FILES["file"])
            return HttpResponseRedirect("/view/")
    else:
        form = UploadGDSFileForm()
    return render(request, "view.html", {"form": form})

class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "upload.html"  # Replace with your template.
    success_url = "success/"  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            ...  # Do something with each file.
        return super().form_valid(form)