import os
import sys
from pathlib import Path

from django.shortcuts import render
from .forms import ModelPredictForm
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import joblib

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))


def svc_model(request, file_path):
    df = pd.read_excel(f"uploads/processed_datasets/{file_path}")
    df['Курс'] = df['Курс'].astype('category')
    if 'Успешность' in df.columns:
        df_prepared = df.drop(['Успешность'], axis=1)
    else:
        df_prepared = df
    df_dummy = pd.get_dummies(df_prepared)
    x_train, y_train, mean_list, std_list = get_train_test_samples(df_dummy)
    clf = SVC(probability=True).fit(x_train, y_train)
    col_list = list(df_dummy.columns)
    save_model(clf, col_list, mean_list, std_list)
    return render(request, 'predict_model_controller/teaching_model_result.html', {'file_path': file_path})


def predict_form(request):
    if request.method == 'POST':
        form = ModelPredictForm(data=request.POST)
        if form.is_valid():
            lock = False
            model, mean_std_list, feature_list = load_model('SVC0')
            params_dict = {'Форма обучения': form.cleaned_data['educ_form'],
                           'Квалификация': form.cleaned_data['qualification'],
                           'Курс': form.cleaned_data['course'],
                           'Профиль': form.cleaned_data['profile'],
                           'Выпуск. отдел.': form.cleaned_data['dep'],
                           'Обуч. подразд.': form.cleaned_data['subdep'],
                           'Форма финансирования': form.cleaned_data['fin'],
                           'Гражданство': form.cleaned_data['citizenship'],
                           'Пол': form.cleaned_data['gender'],
                           'Академ отпуск (действующий) - да / нет': form.cleaned_data['vacation']}
            df = pd.DataFrame(params_dict, index=[0])
            data_dummy = pd.get_dummies(df)
            dummy_values = np.zeros(len(feature_list)).tolist()
            params_keys = list(data_dummy.columns)
            for param in params_keys:
                if param not in feature_list:
                    print("Входные данные не соответствуют требуемым")
                    lock = True
                    break
                else:
                    dummy_values[feature_list.index(param)] = 1
            if lock:
                print("Невозможно выполнить предсказание. Данные numpy формата не сформированы")
                return render(request, 'predict_model_controller/predict_form.html', {'form': form})
            else:
                stud_prob = model.predict_proba([dummy_values])[0]
                print(stud_prob)
                ind_max = np.argmax(stud_prob)

                return render(request, 'predict_model_controller/predict_result.html', {'stud_class': ind_max,
                                                               'stud_prob': stud_prob[ind_max]})
    else:
        form = ModelPredictForm
    return render(request, 'predict_model_controller/predict_form.html', {'form': form})


def norm_data(df_dummy):  # built-in function
    mean_list = []
    std_list = []
    for feature in (df_dummy.columns):
        if str(df_dummy[feature].dtype) == 'int64' or str(df_dummy[feature].dtype) == 'float64':
            mean = np.mean(df_dummy[feature])
            std = np.std(df_dummy[feature])
            df_dummy[feature] = (df_dummy[feature] - mean) / std
            mean_list.append(mean)
            std_list.append(std)
    return mean_list, std_list


def get_train_test_samples(df_dummy):
    target = df_dummy['Класс']
    df_dummy.drop(['Класс'], axis=1, inplace=True)
    mean_list, std_list = norm_data(df_dummy)
    values = df_dummy.values
    x_train, x_test, y_train, y_test = train_test_split(values, target, test_size=1, random_state=42)
    return x_train, y_train, mean_list, std_list


def save_model(model, col_list, mean_list, std_list):
    with open(f'uploads/models/SVC0_feat_l.txt', 'w') as writer:
        for col in col_list:
            writer.write(f"{col}\n")
    # сохраняем в файл веса mean std
    with open(f'uploads/models/SVC0_norm_w.txt', 'w') as writer:
        for i in range(len(mean_list)):
            writer.write(f"{mean_list[i]} {std_list[i]}\n")
    # сохраняем в файл веса модели
    _ = joblib.dump(model, f"uploads/models/SVC0.joblib.pkl")


def load_model(model_name):
    model = joblib.load(f"uploads/models/{model_name}.joblib.pkl")
    mean_std_list = []
    feature_list = []
    with open(f'uploads/models/{model_name}_norm_w.txt', 'r') as reader:
        str_list = reader.read().split('\n')
        for el in str_list:
            if str(el) != '':
                mean_std_list.append([float(el.split(' ')[0]), float(el.split(' ')[1])])
    with open(f'uploads/models/{model_name}_feat_l.txt', 'r') as reader:
        str_list = reader.read().split('\n')
        for el in str_list:
            if str(el) != '':
                feature_list.append(el)
    return model, mean_std_list, feature_list


def dataset_teaching_model(request):
    filelist = os.listdir(path='uploads/datasets')
    processed_filelist = os.listdir(path='uploads/processed_datasets')

    return render(request, 'predict_model_controller/dataset_teaching_model.html', {'filelist': filelist,
                                                           'processed_filelist': processed_filelist})


def teaching_model_info(request):
    return render(request, 'teaching_model_info.html')


def teaching_model_result(request, file_path):
    return render(request, 'predict_model_controller/teaching_model_result.html', {'file_path': file_path})


def predict_result(request):
    return render(request, 'predict_model_controller/predict_result.html')
