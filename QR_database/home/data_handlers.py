from QR_database.settings import BASE_DIR

def handle_uploaded_file(file):
    file_name = file.name
    with open(str(BASE_DIR) + "/home/uploads/gds_file/" + file_name, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)
