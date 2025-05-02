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
from pathlib import Path


def handle_uploaded_file(file):
    """Handles an uploaded gds file by uploading the file to
    the correct location, and then inserting the file information
    into the database."""
    file_name = file.name
    upload_dir = os.path.join(BASE_DIR, "home/uploads/gds_file/")
    file_path = os.path.join(upload_dir, file_name)
    print("Saving to:", file_path)

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
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


def add_sample_to_db(file_name, id, directory_path, debug = False):
    """adds an individual file to the database"""
    detections, debug_image_path = get_detections(directory_path + file_name, debug = debug)
    print(detections)
    im = cv2.imread(directory_path + file_name)
    print(im)
    coords_detected = []
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
            else:
                rand_id = random.randint(-sys.maxsize-1, sys.maxsize)

        print("bouta add")
        for detection in detections:
            print("detected")
            sample_file = sample_images()
            sample_file.gds_file_id = id
            sample_file.file_name = file_name
            sample_file.width = im.shape[1]
            sample_file.height = im.shape[0]
            if "." not in detection.payload:
                print(detection.payload)
                sample_file.row, sample_file.col = int(re.search( ",(.*):U=UL",detection.payload).group(1)), int(detection.payload.split(",")[0])
                sample_file.abs_x = sample_file.row * (qr_size + spacing) + padding
                sample_file.abs_y = sample_file.col * (qr_size + spacing) + padding

            else:
                sample_file.abs_x, sample_file.abs_y = int(re.search(",(.*):U=")),int(detection.payload.split(",")[0])
                sample_file.row = (sample_file.abs_x - padding) / (qr_size + spacing)
                sample_file.col = (sample_file.abs_y - padding) / (qr_size + spacing)
            sample_file.num_codes = len(detections)
            sample_file.img_id = rand_id # unique id for each image that is the same regardless of which qr code is stored
            cursor.execute("Select * FROM home_sample_images WHERE img_id = %s AND gds_file_id = %s", [rand_id, id])
            info = cursor.fetchall()
            if info == []:
                sample_file.is_anchor = True
            else:
                sample_file.is_anchor = False
            sample_file.layer = 1
            coords_detected.append(f"QR code detected at row: {sample_file.row} col: {sample_file.col}")
            sample_file.save()
            print(sample_file)
    return debug_image_path, coords_detected
    
        

def handle_sample_file(file, id, debug = False):
    """Takes in a file and the id of the gds file that it is a sample to,
    and adds that file to the sample folder with the id of the gds file,
    and adds the sample file(s) to the database as well. Handles multiple files
    contained in a single .zip or single files in .png, .jpeg, .jpg, or .jp2 formats
    """
    directory_path = str(BASE_DIR) + "/home/uploads/samples/id=" + id + "/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    debug_images = []

    if ".zip" in file.name:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(directory_path)
            print(zip_ref.infolist())
            for path in zip_ref.infolist():
                print(path.filename)
                if Path(path.filename).suffix not in [".png", ".jpeg", ".jpg", ".jp2"]:
                    os.remove(directory_path + path.filename)
                else:
                    print("addding")
                    debug_path, coords= add_sample_to_db(path.filename, id, directory_path, debug = debug)
                    if debug_path:
                        debug_images.append((debug_path, coords))

    else:
        if Path(file.name).suffix in [".png", ".jpeg", ".jpg", ".jp2"]:
            with open(directory_path + file.name, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            debug_path, coords = add_sample_to_db(file.name, id, directory_path, debug=debug)
            if debug_path:
                debug_images.append((debug_path, coords))
    with connection.cursor() as cursor:
        cursor.execute("UPDATE home_gds_files SET last_updated = %s WHERE id = %s", [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), int(id)])
    print(f'{debug_images=}')
    return debug_images
