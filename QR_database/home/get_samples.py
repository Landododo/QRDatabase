from django.db import connection
#from QR_database.settings import BASE_DIR
from data_handlers import BASE_DIR

def get_samples(id, row, col, abs_pos = False):
    """Returns the file paths of all the files that have the QR code in the specified row
    and column of the QR grid. Will take absolute position (x and y) if abs_pos = True"""
    if not abs_pos:
        with connection.cursor() as cursor:
            cursor.execute("SELECT file_name FROM home_sample_images WHERE row = %s AND col = %s", [row, col])
            info = cursor.fetchall()
            if info == []:
                return ""
            else:
                for i in info:
                    i = BASE_DIR + f"/home/uploads/samples/id={id}/{i}"
                return info
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT file_name FROM home_sample_images WHERE abs_x < %s AND abs_x > %s AND col < %s AND col > %s", [row * 1.01, row * .99, col *1.01, col * .99])
            info = cursor.fetchall()
            if info == []:
                return ""
            else:
                for i in info:
                    i = BASE_DIR + f"/home/uploads/samples/id={id}/{i}"
                return info