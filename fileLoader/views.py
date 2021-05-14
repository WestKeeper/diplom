from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, 'home.html')

def dataprocess(request):
    return render(request, 'dataprocess.html')


def statistics(request):
    return render(request, 'statistics.html')


def chartjs(request):
    return render(request, 'chartjs.html')

def dataframe_statistics(request):
    return render(request, 'dataset_statistics.html')


def dataframe_report(request):
    return render(request, 'dataset_report.html')


def dataframe_teaching_model(request):
    return render(request, 'dataset_teaching_model.html')


def teaching_model_info(request):
    return render(request, 'teaching_model_info.html')


def teaching_model_result(request):
    return render(request, 'teaching_model_result.html')


def predict_form(request):
    return render(request, 'predict_form.html')


def predict_result(request):
    return render(request, 'predict_result.html')


