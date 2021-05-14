import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def file_uploader(request):
    return render(request, 'fileloader/index.html', {'form2': os.listdir(path='uploads/datasets')})


def upload_file(request):
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        handle_uploaded_file(request.FILES['file'])
        return HttpResponse('/')
    # else:
    #     form = UploadFileForm()
    # return render(request, 'fileloader/index.html', {'form2': os.listdir(path='uploads/datasets')})
    return JsonResponse({'post': 'false', 'list': os.listdir(path='uploads/datasets')})


def handle_uploaded_file(f):
    title = f.name
    with open(f'uploads/datasets/{title}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponse('/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'fileloader/index.html', {'form': form, 'list': os.listdir(path='uploads/datasets')})
