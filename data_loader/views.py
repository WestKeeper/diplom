from django.shortcuts import render


def filelist(request):
    return render(request, 'filelist.html')


def dataset(request):
    return render(request, 'dataset.html')
