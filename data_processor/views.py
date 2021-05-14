from django.shortcuts import render, get_object_or_404


def dataprocess(request):
    return render(request, 'dataprocess.html')


def process_result(request):
    return render(request, 'process_result.html')
