from django.core.files.storage import FileSystemStorage


def save_file(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)
    return uploaded_file_url
