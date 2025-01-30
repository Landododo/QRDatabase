from QR_database.settings import BASE_DIR
from django.db import connection
from QR_counter import count_qr_codes
import datetime
import sqlite3
from .models import gds_files
import os
import zipfile


def handle_uploaded_file(file):
    """Handles an uploaded gds file by uploading the file to
    the correct location, and then inserting the file information
    into the database."""
    file_name = file.name
    file_path = str(BASE_DIR) + "/home/uploads/gds_file/" + file_name
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    n, qr_size, qrs_per_row, qrs_per_col = count_qr_codes(file_path)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_file = gds_files()
    new_file.file_name = file_name
    new_file.num_qrs = n
    new_file.qr_size = qr_size
    new_file.qrs_per_row = qrs_per_row
    new_file.qrs_per_col = qrs_per_col
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
    with connection.cursor() as cursor:
        cursor.execute("UPDATE home_gds_files SET last_updated = %s WHERE id = %s", [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(id)])

