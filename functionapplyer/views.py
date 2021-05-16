import os
from django.shortcuts import render, HttpResponse, redirect
import functionapplyer.forms as func_forms
from functionapplyer.forms import FuncFileNameForm
import numpy as np
import pandas as pd
import re



RAW_FILE_CHOICES_DICT = {}
PREP_FILE_CHOICES_DICT = {}
FUNC_CHOICES_DICT = {1: 'encode_personal_data',
                     2: 'drop_unnecessary_cols',
                     3: 'delete_extra_disciplines',
                     4: 'delete_linear_dependencies',
                     5: 'clean_outliers',
                     6: 'clean_missings_dropna',
                     7: 'clean_missings_fillna',
                     8: 'reformat_cols_type',
                     9: 'create_target_vars'}


def filedict_choice_update(path, filename):
    x = globals()
    x[filename] = {}
    tmp = os.listdir(path=path)
    inc = 1
    for el in tmp:
        x[filename][inc] = el
        inc += 1


def func_pipeline(request):
    category_cols = ['Форма обучения', 'Квалификация', 'Курс', 'Специальность',
                     'Профиль', 'Выпуск. отдел.', 'Выпуск. школа', 'Группа',
                     'Обуч. подразд.', 'Форма финансирования', 'Страна', 'Гражданство',
                     'Пол', 'Дата рождения', 'Академ отпуск (действующий) - да / нет',
                     'Дисциплины по которым получены неудовлетворительные оценки']
    numeric_cols = ['Всего', 'Положительных', 'Неудовлетворительных',
                    'Пропусков по дисциплинам по которым получены неудовлетворительные оценки',
                    'Всего часов по дисциплинам по которым получены неудовлетворительные оценки',
                    'Всего часов пропусков в семестре', 'Всего часов аудиторных занятий в семестре']
    filedict_choice_update('uploads/datasets', 'RAW_FILE_CHOICES_DICT')
    filedict_choice_update('uploads/datasets_prepared', 'PREP_FILE_CHOICES_DICT')
    raw_filename = ''
    prep_filename = ''
    if request.method == 'POST':
        form = FuncFileNameForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data.get('raw_file_name')
            if str(cd) == '':
                cd = form.cleaned_data.get('prep_file_name')
                if str(cd) == '':
                    return HttpResponse('Need to choose a file')
                else:
                    prep_filename = PREP_FILE_CHOICES_DICT.get(int(form.cleaned_data.get('prep_file_name')))  # a dictKey expected
            else:
                raw_filename = RAW_FILE_CHOICES_DICT.get(int(form.cleaned_data.get('raw_file_name')))  # a dictKey expected
            dictkey_list = form.cleaned_data.get('func_name')  # a list of dictKeys expected
            funcnames = []
            for t in dictkey_list:
                funcnames.append(FUNC_CHOICES_DICT.get(int(t)))
            if funcnames is []:
                return HttpResponse('Need to choose functions')
            if raw_filename == '':
                df = pd.read_excel(f"uploads/datasets_prepared/{prep_filename}")
                temp_list = prep_filename.split('.')[:-1]
            else:
                df = pd.read_excel(f"uploads/datasets/{raw_filename}")
                temp_list = raw_filename.split('.')[:-1]

            string = ''
            for element in temp_list:
                string += element

            # if statements
            if 'encode_personal_data' in funcnames:
                encode_personal_data(df)
                string += f'-EPD'

            if 'drop_unnecessary_cols' in funcnames:
                unnecessary_cols_list = ['Дата рождения', 'Выпуск. школа']  # здесь должен быть request
                drop_unnecessary_cols(df, unnecessary_cols_list)
                for col in unnecessary_cols_list:
                    if col in category_cols:
                        category_cols.remove(col)
                    elif col in numeric_cols:
                        numeric_cols.remove(col)
                string += f'-DUC'

            if 'delete_linear_dependencies' in funcnames:
                delete_linear_dependencies(df)
                string += f'-DLD'

            if 'clean_outliers' in funcnames:
                clean_outliers(df, numeric_cols)
                string += f'-CO'

            if 'clean_missings_dropna' in funcnames:
                clean_missings_dropna(df)
                string += f'-CMD'

            if 'clean_missings_fillna' in funcnames:
                clean_missings_fillna(df, category_cols, numeric_cols)
                string += f'-CMF'

            if 'delete_extra_disciplines' in funcnames:
                delete_extra_disciplines(df)
                string += f'-DED'

            if 'reformat_cols_type' in funcnames:
                reformat_cols_type(df, category_cols, numeric_cols)
                string += f'-RCT'

            if 'create_target_vars' in funcnames:
                create_target_vars(df)
                string += f'-CTV'
            # end if statements

            # for func in funcnames:
            #     df_new = func_dict[func](df_new)
            #     string += f'-{func}'

            df.to_excel(f"uploads/datasets_prepared/{string}.xlsx", index=False)

            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = FuncFileNameForm()
    func_forms.filestorage_update_activator()
    # form.set_raw_file_name(func_forms.RAW_FILE_CHOICES)
    # form.set_prep_file_name(func_forms.PREP_FILE_CHOICES)
    return render(request, 'fileloader/index.html', {'func_file_name': form})


def encode_personal_data(df):
    df['Индекс студента'] = range(len(df))
    df.drop(['Фамилия', 'Имя', 'Отчество'], axis=1, inplace=True)


def drop_unnecessary_cols(df, unnecessary_cols_list):
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
        bin_column = df['Дисциплины по которым получены неудовлетворительные оценки']\
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
