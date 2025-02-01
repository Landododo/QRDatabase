from django.db import connection
from settings import BASE_DIR

def get_samples(row, col, abs_pos = False):
    """Returns the file paths of all the files that have the QR code in the specified row
    and column of the QR grid. Will take absolute position (x and y) if abs_pos = True"""
    if not abs_pos:
        with connection.cursor() as cursor:
            cursor.execute("SELECT file_name FROM home_sample_images WHERE row = %s AND col = %s", [row, col])
            info = cursor.fetchall()
            if info == []:
                return ""
            else:
                return 
    else:
        return None