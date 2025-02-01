from QR_database.settings import BASE_DIR
from django.db import connection
from QR_counter import count_qr_codes
import datetime
import sqlite3
from .models import gds_files, sample_images
import os
import zipfile
from detection.main import get_detections
import cv2,random, sys, re

def handle_uploaded_file(file):
    """Handles an uploaded gds file by uploading the file to
    the correct location, and then inserting the file information
    into the database."""
    file_name = file.name
    file_path = str(BASE_DIR) + "/home/uploads/gds_file/" + file_name
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    n, qr_size, qrs_per_row, qrs_per_col, spacing,padding = count_qr_codes(file_path)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_file = gds_files()
    new_file.file_name = file_name
    new_file.num_qrs = n
    new_file.qr_size = qr_size
    new_file.qrs_per_row = qrs_per_row
    new_file.qrs_per_col = qrs_per_col
    new_file.spacing = spacing
    new_file.padding = padding
    new_file.time_uploaded = now
    new_file.last_updated = now
    new_file.save()


def handle_sample_file(file, id):
    directory_path = str(BASE_DIR) + "/home/uploads/samples/id=" + id + "/"
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    if ".zip" in file.name:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(directory_path)
    else:
        with open(directory_path + file.name, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        detections = get_detections(directory_path + file.name)
        im = cv2.imread(directory_path + file.name)
        with connection.cursor() as cursor:
            # get information from the gds file (used to calculate qr code position)
            cursor.execute("SELECT qr_size, spacing, padding FROM home_gds_files WHERE id = %s", [id])
            qr_size, spacing, padding = cursor.fetchall()[0]
            rand_id = random.randint(-sys.maxsize-1, sys.maxsize)
            unique_id = False
            while unique_id == False:
                cursor.execute("Select * FROM home_gds_files WHERE id = %s", [rand_id])
                info = cursor.fetchall()
                if info == []:
                    unique_id = True

            for detection in detections:
                sample_file = sample_images()
                sample_file.gds_file_id = id
                sample_file.file_name = file.name
                sample_file.width = im.shape[1]
                sample_file.height = im.shape[0]
                if "." not in detection.payload:
                    sample_file.row, sample_file.col = int(re.search( ",(.*):U=UL",detection.payload).group(1)), int(detection.payload.split(",")[0])
                    sample_file.abs_x = sample_file.row * (qr_size + spacing) + padding
                    sample_file.abs_y = sample_file.col * (qr_size + spacing) + padding

                else:
                    sample_file.abs_x, sample_file.abs_y = int(re.search(",(.*):U=")),int(detection.payload.split(",")[0])
                    sample_file.row = (sample_file.abs_x - padding) / (qr_size + spacing)
                    sample_file.col = (sample_file.abs_y - padding) / (qr_size + spacing)
                sample_file.num_codes = len(detections)
                sample_file.img_id = rand_id # unique id for each image that is the same regardless of which qr code is stored
                sample_file.save()
    with connection.cursor() as cursor:
        cursor.execute("UPDATE home_gds_files SET last_updated = %s WHERE id = %s", [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(id)])

