from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from .forms import UploadGDSFileForm, FileFieldForm, MultipleFileField
from django.views.generic.edit import FormView
from django import forms
from .data_handlers import handle_uploaded_file, handle_sample_file
from django.db import connection
from .models import gds_files
from django.conf import settings
from pathlib import Path

# Create your views here.
def index(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'home.html')
# # gets api file list for React t ouse
# def api_file_list(request):
#     return JsonResponse(file_list(), safe=False)

# def api_sample_list(request):
#     row = request.GET.get("row")
#     col = request.GET.get("col")
#     if row is not None and col is not None:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM home_sample_images WHERE row = %s AND col = %s", [row, col])
#             results = cursor.fetchall()
#         return JsonResponse([
#             {
#                 "gds_file_id": r[1],
#                 "file_name": r[2],
#                 "row": r[5],
#                 "col": r[6],
#                 "img_id": r[10]
#             }
#             for r in results
#         ], safe=False)
#     else:
#         return JsonResponse([], safe=False)

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
    def get_success_url(self):
        return f"/view/{self.kwargs['gds_file_id']}/"
    
    def get_context_data(self, **kwargs):
        # Get default context from parent class
        context = super().get_context_data(**kwargs)
        gds_file_id = self.kwargs.get("gds_file_id")  # ✅ extract from URL

        # Add additional data to the context
        context["file_list"] = file_list()
        context["samples"] = sample_list()
        context["gds_file_id"] = gds_file_id  # ✅ pass to template

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
        context["debug_images"] = getattr(self, 'debug_images', [])
        print(context)
        return context
    
    def form_valid(self, form):
        print("doing something")
        files = tuple(self.request.FILES.getlist("file_field"))
        id = self.request.POST.get('document-select')
        debug = self.request.POST.get("debug") == "true"

        if debug:
            entries = []
            DEBUG_DIRECTORY = "./debug/scanner/"
            self.debug_images = [] # initialize list of empty debug images to show
            for f in files:
                for rel_path, coords in handle_sample_file(f, id, debug=True):
                    entries.append({
                        "img":    rel_path,   # 'debug/scanner/foo.png'
                        "coords": coords,               # list[str]
                    })
                print(f)
                print(f'{debug=}')
                # handle_sample_file(f, id, debug)
                # debug_path = DEBUG_DIRECTORY + f"{f.name.split("/")[-1].split(".")[0]}_detections.png"
                # debug_images.append(debug_path)
                # debug_paths = handle_sample_file(f, id, debug)
                self.debug_images = entries
            print(self.debug_images)
            return self.render_to_response(self.get_context_data())
        else:
            for f in files:
                print(f)
                print(f'{debug=}')
                handle_sample_file(f, id, debug)
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

def view_qr_images(request, row, col, gds_id):
    with connection.cursor() as cursor:
        print(f"Fetching images for row={row}, col={col}, gds_id={gds_id}")
        cursor.execute("SELECT * FROM home_sample_images WHERE row = %s AND col = %s AND gds_file_id = %s", [row, col, gds_id])
        results = cursor.fetchall()
        print(f'{results=}')

    image_list = [
        {
            "file_name": r[2],
            "gds_file_id": r[1],
            "img_id": r[10],
        }
        for r in results
    ]

    return render(request, "view_qr_images.html", {
        "row": row,
        "col": col,
        "images": image_list,
        "gds_file_id": gds_id
    })

from QR_database.settings import BASE_DIR
import os
def upload_sample_file(request, gds_id, row, col):
    if request.method == "POST":
        uploaded_file = request.FILES['file_field']
        directory_path = str(BASE_DIR) + f"/home/uploads/samples/id={gds_id}/"

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        file_path = os.path.join(directory_path, uploaded_file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Now you should also create a database record linking it to (row, col)
        # Insert into sample_images
        from .models import sample_images
        from django.db import connection
        import random
        import sys

        # Example of creating the sample_images record manually:
        with connection.cursor() as cursor:
            rand_id = random.randint(-sys.maxsize-1, sys.maxsize)
            unique_id = False
            while unique_id == False:
                cursor.execute("Select * FROM home_gds_files WHERE id = %s", [rand_id])
                info = cursor.fetchall()
                if info == []:
                    unique_id = True
                else:
                    rand_id = random.randint(-sys.maxsize-1, sys.maxsize)
            cursor.execute("""
                INSERT INTO home_sample_images
                (gds_file_id, file_name, width, height, row, col, abs_x, abs_y, num_codes, img_id, is_anchor, layer)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                gds_id,
                uploaded_file.name,
                0, 0,  # Width and height can be 0 for non-images
                row,
                col,
                0, 0,  # abs_x, abs_y can be 0 or computed if needed
                0,  # num_codes
                rand_id,  # img_id
                1,  # is_anchor
                1   # layer
            ])

        return HttpResponseRedirect(f"/view_qr/{gds_id}/{row}/{col}/")