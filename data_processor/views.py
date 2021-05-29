import os

from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from .forms import DataProcessForm, DatasetForm

import numpy as np
import pandas as pd
import re


def dataset_process(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            file_name = form.cleaned_data['dataset']
            return redirect('data_processor:dataprocess', file_name)
    else:
        form = DatasetForm
    return render(request, 'data_processor/dataset_process.html', {'form': form})


def dataprocess(request, file_name):
    category_cols = ['Форма обучения', 'Квалификация', 'Курс', 'Специальность',
                     'Профиль', 'Выпуск. отдел.', 'Выпуск. школа', 'Группа',
                     'Обуч. подразд.', 'Форма финансирования', 'Страна', 'Гражданство',
                     'Пол', 'Дата рождения', 'Академ отпуск (действующий) - да / нет',
                     'Дисциплины по которым получены неудовлетворительные оценки']
    numeric_cols = ['Всего', 'Положительных', 'Неудовлетворительных',
                    'Пропусков по дисциплинам по которым получены неудовлетворительные оценки',
                    'Всего часов по дисциплинам по которым получены неудовлетворительные оценкЫи',
                    'Всего часов пропусков в семестре', 'Всего часов аудиторных занятий в семестре']
    if request.method == 'POST':
        form = DataProcessForm(file_name, request.POST)
        if form.is_valid():
            df = pd.read_excel(f"uploads/datasets/{file_name}")
            temp_list = file_name.split('.')[:-1]
            name_without_ext = ''
            for element in temp_list:
                name_without_ext += element

            # if statements
            if form.cleaned_data['personal'] == "Обработать персональные данные":
                encode_personal_data(df)
                name_without_ext += f'-EPD'

            if form.cleaned_data['linear_dep'] == "Исключить линейные зависимости":
                delete_linear_dependencies(df)
                name_without_ext += f'-DLD'

            cols_to_del = []
            for numeric_col in numeric_cols:
                if numeric_col not in df.columns:
                    cols_to_del.append(numeric_col)
            numeric_cols = list(set(numeric_cols) - set(cols_to_del))

            if form.cleaned_data['outlayers'] == "Удалить записи с выбросом":
                clean_outliers(df, numeric_cols)
                name_without_ext += f'-CO'

            if form.cleaned_data['missing'] == "Удалить запись с миссингом":
                clean_missings_dropna(df)
                name_without_ext += f'-CMD'

            if form.cleaned_data['missing'] == "Заменить медианой признака для числовых, категорией \"Нет\" " \
                                               "для категориальных признаков":
                clean_missings_fillna(df, category_cols, numeric_cols)
                name_without_ext += f'-CMF'

            if form.cleaned_data['facult'] == "Удалить факультативы":
                delete_extra_disciplines(df)
                name_without_ext += f'-DED'

            # reformat_cols_type
            reformat_cols_type(df, category_cols, numeric_cols)

            if form.cleaned_data['target_val'] == "Сформировать целевые переменные":
                create_target_vars(df)
                name_without_ext += f'-CTV'

            if form.cleaned_data['hand_not_inf']:
                drop_unnecessary_cols(df, form.cleaned_data['hand_not_inf'])
                for col in form.cleaned_data['hand_not_inf']:
                    if col in category_cols:
                        category_cols.remove(col)
                    elif col in numeric_cols:
                        numeric_cols.remove(col)
                name_without_ext += f'-HDUC'


            # automatic not-informative columns processing
            if form.cleaned_data['not_inf'] == "Обработать неинформативные признаки":
                unnecessary_cols_list = ['Дата рождения', 'Всего', 'Положительных', 'Неудовлетворительных',
                                         'Группа', 'Страна', 'Дисциплина по которым получены неудовлетворительные оценки',
                                         'Индекс студента', 'Выпуск. школа',
                                         'Всего часов по дисциплинам по которым получены неудовлетворительные оценки',
                                         'Пропусков по дисциплинам по которым получены неудовлетворительные оценки',
                                         'Всего часов пропусков в семестре', 'Всего аудиторных занятий в семестре']
                drop_unnecessary_cols(df, unnecessary_cols_list)
                for col in unnecessary_cols_list:
                    if col in category_cols:
                        category_cols.remove(col)
                    elif col in numeric_cols:
                        numeric_cols.remove(col)
                name_without_ext += f'-DUC'

            df.to_excel(f"uploads/processed_datasets/{name_without_ext}.xlsx", index=False)

            return render(request, 'data_processor/process_result.html', {'file_name': f'{name_without_ext}.xlsx'})
    else:
        form = DataProcessForm(file_name)
    return render(request, 'data_processor/dataprocess.html', {'form': form, 'file_name': file_name})


def encode_personal_data(df):
    df['Индекс студента'] = range(len(df))
    df.drop(['Фамилия', 'Имя', 'Отчество'], axis=1, inplace=True)


def drop_unnecessary_cols(df, unnecessary_cols_list):
    cols_to_del = []
    for col in unnecessary_cols_list:
        if col not in df.columns:
            cols_to_del.append(col)
    unnecessary_cols_list = list(set(unnecessary_cols_list) - set(cols_to_del))
    df.drop(unnecessary_cols_list, axis=1, inplace=True)


def clean_missings_dropna(df):
    df.dropna(inplace=True)
    df.reset_index(inplace=True)


def clean_missings_fillna(df, category_cols, numeric_cols):
    for cat_col in category_cols:
        df[cat_col].fillna(value='Нет', inplace=True)
    for col in numeric_cols:
        df[col].fillna(value=df[col].median(), inplace=True)


def reformat_cols_type(df, category_cols, numeric_cols):
    df[category_cols].astype('category')
    df[numeric_cols].astype(float)


def clean_outliers(df, numeric_cols):
    # IQR (interquartile range) = Q3-Q1  # Q1 - 1.5*IQR  # Q3 + 1.5*IQR
    df_quarntiled = df[numeric_cols].quantile([.25, .75])
    for num_col in list(df_quarntiled.columns):
        median = df[num_col].median()
        quantiles = df[num_col].values
        iqr = quantiles[1] - quantiles[0]
        left_mustache = quantiles[0] - 1.5 * iqr
        right_mustache = quantiles[1] + 1.5 * iqr
        for i in range(len(df)):
            if left_mustache < df[num_col][i] < right_mustache:
                df[num_col][i] = median


def delete_extra_disciplines(df):
    facult_list = ['Второй иностранный язык \(немецкий\). А2.1\(Зач.\),[.]?',
                   'Второй иностранный язык \(немецкий\). А2.1\(Зач.\)[.]?',
                   'Второй иностранный язык \(немецкий\). А1.1\(Зач.\),[.]?',
                   'Второй иностранный язык \(немецкий\). А1.1\(Зач.\)[.]?',
                   'Второй иностранный язык \(китайский\). 1\(Зач.\),[.]?',
                   'Второй иностранный язык \(китайский\). 1\(Зач.\)[.]?',
                   'Второй иностранный язык \(французский\). А1.1\(Зач.\),[.]?',
                   'Второй иностранный язык \(французский\). А1.1\(Зач.\)[.]?',
                   'Иностранный язык для программ академической мобильности \(английский\). А2.2\(Зач.\),[.]?',
                   'Иностранный язык для программ академической мобильности \(английский\). А2.2\(Зач.\)[.]?',
                   'Управление проектами\(Зач.\),[.]?', 'Управление проектами\(Зач.\)[.]?',
                   'Факультативные дисциплины по выбору студента\(Зач.\),[.]?',
                   'Факультативные дисциплины по выбору студента\(Зач.\)[.]?',
                   'Креативность инженера\(Зач.\),[.]?', 'Креативность инженера\(Зач.\)[.]?']

    def discount(strings):
        if len(re.findall(strings[0], strings[1])) == 0:
            return 0
        else:
            return 1

    for facult in facult_list:
        bin_column = df['Дисциплины по которым получены неудовлетворительные оценки'] \
            .apply(lambda s: discount([facult, s]))
        df[['Всего', 'Неудовлетворительных']] = df[['Всего', 'Неудовлетворительных']].sub(bin_column, axis=0)
        df.replace({facult: ''}, inplace=True, regex=True)

    df.replace(r'^\s*$', np.nan, inplace=True, regex=True)
    df['Дисциплины по которым получены неудовлетворительные оценки'] = df[
        'Дисциплины по которым получены неудовлетворительные оценки'].str.strip()
    df.replace({' +': ' '}, inplace=True, regex=True)
    df['Дисциплины по которым получены неудовлетворительные оценки'].fillna('Нет', inplace=True)


def delete_linear_dependencies(df):
    corr = df.corr()
    column_list = list(corr.columns)
    for j in range(len(column_list)):
        for i in range(len(column_list)):
            if j == i:
                break
            if corr[column_list[j]][i] > 0.75:
                df.drop(column_list[j], axis=1, inplace=True)


def create_target_vars(df):
    df['Успешность'] = df['Положительных'] / df['Всего']

    def classify(success):
        if success >= 0.75:
            return 2
        elif success > 0.25:
            return 1
        else:
            return 0

    df['Класс'] = df['Успешность'].apply(classify)


# def dataprocess(request):
#     filelist = os.listdir(path='uploads/datasets')
#     processed_filelist = os.listdir(path='uploads/processed_datasets')
#     filelist += processed_filelist
#     if request.method == 'POST':
#         form = DataProcessForm(request.POST)
#         if form.is_valid():
#             return render(request, 'filelist.html', {'form': form, 'filelist': filelist})
#         else:
#             return render(request, 'dataprocess.html', {'form': form, 'filelist': filelist})
#     else:
#         form = DataProcessForm
#         return render(request, 'dataprocess.html', {'form': form, 'filelist': filelist})


def process_result(request):
    return render(request, 'data_processor/process_result.html')
