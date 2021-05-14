import os
from django.shortcuts import render, HttpResponse, redirect
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from functionapplyer import views as func_views
from functionapplyer import forms as func_forms
import pandas as pd
import joblib


def svc_model(request):
    raw_filename = ''
    prep_filename = ''
    if request.method == 'POST':
        form = func_forms.FuncFileNameForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data.get('raw_file_name')
            if str(cd) == '':
                cd = form.cleaned_data.get('prep_file_name')
                if str(cd) == '':
                    return HttpResponse('Need to choose a file')
                else:
                    prep_filename = func_views.PREP_FILE_CHOICES_DICT.get(
                        int(form.cleaned_data.get('prep_file_name')))  # a dictKey expected
            else:
                raw_filename = func_views.RAW_FILE_CHOICES_DICT.get(
                    int(form.cleaned_data.get('raw_file_name')))  # a dictKey expected
            if raw_filename == '':
                df = pd.read_excel(f"uploads/datasets_prepared/{prep_filename}")
                temp_list = prep_filename.split('.')[:-1]
            else:
                df = pd.read_excel(f"uploads/datasets/{raw_filename}")
                temp_list = raw_filename.split('.')[:-1]

            string = ''
            for element in temp_list:
                string += element

            x_train, x_test, y_train, y_test = get_train_test_samples(df)
            answers = []
            min_val = 5
            max_val = 10
            for i in range(min_val, max_val):
                clf = SVC(i).fit(x_train, y_train)
                answers.append(test(clf, x_test, y_test))
            max_ans_idx = answers.index(max(answers)) + min_val
            clf = SVC(max_ans_idx).fit(x_train, y_train)
            save_model(clf)
    else:
        form3 = func_forms.FuncFileNameForm()
    # func_forms.filestorage_update_activator()
    return render(request, 'fileloader/index.html', {'func_file_name': form3})


def get_train_test_samples(df):
    data_dummy = pd.get_dummies(df)
    target = data_dummy['Класс']
    data_dummy.drop(['Класс'], axis=1, inplace=True)
    values = data_dummy.values
    X_train, X_test, y_train, y_test = train_test_split(values, target, test_size=0.33, random_state=42)
    return X_train, X_test, y_train, y_test


def test(model, x_test, y_test):
    return model.score(x_test, y_test)


def predict(model, sample):
    return model.predict(sample)


def save_model(model):
    _ = joblib.dump(model, "uploads/models")


def load_model(model_name):
    return joblib.load(f"uploads/models/{model_name}")
