from django.shortcuts import render


def teaching_model_info(request):
    return render(request, 'teaching_model_info.html')


def teaching_model_result(request):
    return render(request, 'teaching_model_result.html')


def predict_form(request):
    return render(request, 'predict_form.html')


def predict_result(request):
    return render(request, 'predict_result.html')

