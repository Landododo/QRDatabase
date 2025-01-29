from QR_database.settings import BASE_DIR
from django.db import connection
from QR_counter import count_qr_codes
import datetime

def handle_uploaded_file(file):
    file_name = file.name
    file_path = str(BASE_DIR) + "/home/uploads/gds_file/" + file_name
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
    n, qr_size, qrs_per_row, qrs_per_col = count_qr_codes(file_path)
    with connection.cursor() as cursor:
        cursor.execute("CREATE TABLE gds_files (file_name varchar(255), num_qrs int, qr_size REAL, qrs_per_row int, qrs_per_col int, time_uploaded TEXT, last_updated TEXT)")
        cursor.execute("INSERT INTO gds_files (file_name, num_qrs, qr_size, qrs_per_row, qrs_per_col,time_uploaded, last_updated)"\
                       +f" Values ({file_name},{n},{qr_size},{qrs_per_row},{qrs_per_col}, {datetime.datetime.now()},{datetime.datetime.now()})"
                       )

def handle_uploaded_files(files):
    for file in files:
        with open(str(BASE_DIR) + "/home/uploads/samples/" + file.name, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

