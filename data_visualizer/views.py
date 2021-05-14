from django.shortcuts import render
# Create your views here.

def statistics(request):
    return render(request, 'statistics.html')


def dataset_statistics(request):
    return render(request, 'dataset_statistics.html')
