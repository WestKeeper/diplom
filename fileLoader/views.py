from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, 'home.html')


def filelist(request):
    return render(request, 'filelist.html')


def dataprocess(request):
    return render(request, 'dataprocess.html')


def statistics(request):
    return render(request, 'statistics.html')


def chartjs(request):
    return render(request, 'chartjs.html')
