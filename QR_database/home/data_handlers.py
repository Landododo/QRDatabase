def handle_uploaded_file(request):
    file_name = request.title
    with open("user_data.txt", 'w') as f:
        f.write(request.file)
    print(request)
    return None