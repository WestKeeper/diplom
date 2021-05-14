from django.shortcuts import render


def report_result(request):
    return render(request, 'report_result.html')
