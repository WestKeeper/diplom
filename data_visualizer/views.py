import copy
import math
import json
import os
import sys
from pathlib import Path

from django.shortcuts import render

import pandas as pd
import scipy.stats

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

cat_cols = ['Форма обучения', 'Квалификация', 'Курс', 'Специальность', 'Профиль',
            'Выпуск. отдел.', 'Выпуск. школа', 'Группа', 'Обуч. подразд.',
            'Фамилия', 'Имя', 'Отчество', 'Форма финансирования', 'Страна',
            'Гражданство', 'Пол', 'Дата рождения',
            'Академ отпуск (действующий) - да / нет',
            'Дисциплины по которым получены неудовлетворительные оценки', 'Класс']
num_cols = ['Всего', 'Положительных', 'Неудовлетворительных',
            'Пропусков по дисциплинам по которым получены неудовлетворительные оценки',
            'Всего часов по дисциплинам по которым получены неудовлетворительные оценки',
            'Всего часов пропусков в семестре',
            'Всего часов аудиторных занятий в семестре', 'Успешность']


def statistics(request, file_path):
    df = pd.read_excel(f'uploads/datasets/{file_path}')
    df_cols = df.columns
    df_list = []
    for i, ind in enumerate(list(df.describe().index)):
        df_list.append([ind] + list(df.describe().values[i]))
    desc_cols = df.describe().columns

    df_cat_cols = []
    df_num_cols = []
    p_list = []

    for cat_col in cat_cols:
        if cat_col in df_cols:
            p_value1, p_value2, i_norm, pval, feature, feature_value = build_hypothises(df, cat_col)
            if p_value1 is None:
                print('p value is None')
                continue
            df_cat_cols.append(
                cat_col.replace('(', '_').replace(')', '_').replace('/', '').replace('.', '_').replace('-',
                                                                                                       '_').replace(' ',
                                                                                                                    '_'))
            histogram_builder(df, cat_col)
            p_list.append({'p_value1': p_value1, 'p_value2': p_value2,
                           'i_norm': i_norm, 'pval': pval,
                           'feature': feature.replace('(', '_').replace(')', '_').replace('/', '').replace(
                               '.', '_').replace('-', '_').replace(' ', '_'),
                           'feature_value': feature_value})

    for num_col in num_cols:
        if num_col in df_cols:
            df_num_cols.append(
                num_col.replace('(', '_').replace(')', '_').replace('/', '').replace('.', '_').replace('-',
                                                                                                       '_').replace(' ',
                                                                                                                    '_'))
            histogram_builder(df, num_col)
            boxplot_builder(df, num_col)

    return render(request, 'data_visualizer/statistics.html', {'df_list': df_list,
                                               'df_cols': [''] + list(df_cols),
                                               'desc_cols': [''] + list(desc_cols),
                                               'df_cat_cols': df_cat_cols,
                                               'df_num_cols': df_num_cols,
                                               'p_list': p_list})


def processed_statistics(request, file_path):
    df = pd.read_excel(f'uploads/processed_datasets/{file_path}')
    df_cols = df.columns
    df_list = []
    for i, ind in enumerate(list(df.describe().index)):
        df_list.append([ind] + list(df.describe().values[i]))
    desc_cols = df.describe().columns

    df_cat_cols = []
    df_num_cols = []
    p_list = []

    for cat_col in cat_cols:
        if cat_col in df_cols:
            p_value1, p_value2, i_norm, pval, feature, feature_value = build_hypothises(df, cat_col)
            if p_value1 is None:
                print('p value is None')
                continue
            df_cat_cols.append(
                cat_col.replace('(', '_').replace(')', '_').replace('/', '').replace('.', '_').replace('-',
                                                                                                       '_').replace(' ',
                                                                                                                    '_'))
            histogram_builder(df, cat_col)
            p_list.append({'p_value1': p_value1, 'p_value2': p_value2,
                           'i_norm': i_norm, 'pval': pval,
                           'feature': feature.replace('(', '_').replace(')', '_').replace('/', '').replace(
                               '.', '_').replace('-', '_').replace(' ', '_'),
                           'feature_value': feature_value})

    for num_col in num_cols:
        if num_col in df_cols:
            df_num_cols.append(
                num_col.replace('(', '_').replace(')', '_').replace('/', '').replace('.', '_').replace('-',
                                                                                                       '_').replace(' ',
                                                                                                                    '_'))
            histogram_builder(df, num_col)
            boxplot_builder(df, num_col)

    return render(request, 'data_visualizer/statistics.html', {'df_list': df_list,
                                               'df_cols': [''] + list(df_cols),
                                               'desc_cols': [''] + list(desc_cols),
                                               'df_cat_cols': df_cat_cols,
                                               'df_num_cols': df_num_cols,
                                               'p_list': p_list})


def dataset_stat(request):
    filelist = os.listdir(path='uploads/datasets')
    processed_filelist = os.listdir(path='uploads/processed_datasets')
    return render(request, 'data_visualizer/dataset_stat.html', {'filelist': filelist,
                                                 'processed_filelist': processed_filelist})


# content = [ list(labels), [(str(label), list(data)] ]
def linechart_to_json(content, index):
    labels = content[0]
    datasets = []
    for el in content[1]:
        datasets.append({
            "label": el[0],
            "data": el[1]
        })
    areaChartData = {"labels": labels, "datasets": datasets}
    write_to_file(f"{ROOT_DIR}\\chart-txt\\LineChartData-{index}.txt",
                  f"LineChartData{index} = '[{json.dumps(areaChartData)}]'")


# uploads/json/LinearChartData.txt


# content = [ list(labels), [(str(label), list(data)] ]
def barchart_to_json(content, index):
    labels = content[0]
    datasets = []
    for el in content[1]:
        datasets.append({
            "label": el[0],
            "data": el[1]
        })
    areaChartData = {"labels": labels, "datasets": datasets}
    write_to_file(f"{ROOT_DIR}\\static\\chart-txt\\BarChartData-{index}.txt",
                  f"BarChartData{index} = '[{json.dumps(areaChartData)}]'")


# content = [ list(labels), list(line_data), str(label), list(data) ]
# data = {int(x), int(y)}
def q_q_plot_to_json(content, index):
    labels = content[0]
    line_data = content[1]
    label = content[2]
    data = content[3]
    areaChartData = {"labels": labels, "line_data": line_data, "label": label, "scatter_data": data}
    write_to_file(f"{ROOT_DIR}\\static\\chart-txt\\QQChartData-{index}.txt",
                  f"QQChartData{index} = '[{json.dumps(areaChartData)}]'")


# content = [ str(x), int(low), int(q1), int(median), int(q3), int(high), list(outliers)]
# if Q3 + 1.5*IQR < value < Q1 - 1.5*IQR:
# outliers.append(value)
def boxplot_to_json(content, index):
    data = []
    for el in content:
        data.append({"x": el[0], "low": el[1], "q1": el[2],
                     "median": el[3], "q3": el[4], "high": el[5], "outliers": el[6]})
    areaChartData = {"data": data}
    write_to_file(f"{ROOT_DIR}\\static\\chart-txt\\BoxplotChartData-{index}.txt",
                  f"BoxplotChartData{index} = '[{json.dumps(areaChartData)}]'")


# content = [ list(labels), str(label), list(data) ]
def catplot_to_json(content, index):
    labels = content[0]
    label = content[1]
    datasets = content[2]
    areaChartData = {"labels": labels, "label": label, "datasets": datasets}
    write_to_file(f"{ROOT_DIR}\\static\\chart-txt\\CatplotChartData-{index}.txt",
                  f"CatplotChartData{index} = '[{json.dumps(areaChartData)}]'")


def write_to_file(filepath, string):
    with open(filepath, 'w+', encoding="utf-8") as writer:
        writer.write(string)


# histogram

def histogram_builder(df, cat_feature):
    labels = list(df[cat_feature].unique())
    label = f'Гистограмма распределения признака {cat_feature}'
    bar_chart_data = list(df[cat_feature].value_counts().values)
    zip_list = zip(labels, bar_chart_data)
    zip_list = sorted(zip_list)
    res_list = [[i for i, j in zip_list],
                [j for i, j in zip_list]]
    labels = res_list[0]
    bar_chart_data = res_list[1]

    if str(type(labels[0])) == "<class 'numpy.int64'>":
        labels_np_dtype = copy.copy(labels)
        labels = []
        for l in labels_np_dtype:
            labels.append(int(l))

    if str(type(bar_chart_data[0])) == "<class 'numpy.int64'>":
        bar_chart_data_np_dtype = copy.copy(bar_chart_data)
        bar_chart_data = []
        for dat in bar_chart_data_np_dtype:
            bar_chart_data.append(int(dat))

    bar_chart_content = [labels, [(label, bar_chart_data)]]
    barchart_to_json(bar_chart_content,
                     cat_feature.replace('(', '_').replace(')', '_').replace('/', '').replace(
                         '.', '_').replace('-', '_').replace(' ', '_'))


# boxplot
# content = [ str(x), int(low), int(q1), int(median), int(q3), int(high), list(outliers)]
def boxplot_builder(df, num_feature):
    x = "1"
    q1 = df[num_feature].quantile(.25)
    median = df[num_feature].quantile(.5)
    q3 = df[num_feature].quantile(.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    if low < 0:
        low = 0
    high = q3 + 1.5 * iqr
    outliers = []
    for value in df[num_feature]:
        if value < low or value > high:
            outliers.append(value)

    boxplot_content = [[x, low, q1, median, q3, high, outliers]]
    boxplot_to_json(boxplot_content,
                    num_feature.replace('(', '_').replace(')', '_').replace('/', '').replace(
                        '.', '_').replace('-', '_').replace(' ', '_'))


# q-q plot


# slope, intercept, r
# = slope*x + intercept

def qq_plot_builder(df, cat_feature):
    df_grouped = df[[cat_feature, 'Успешность']].groupby(cat_feature).mean()
    feature_value = list(df_grouped[df_grouped['Успешность'] == max(df_grouped['Успешность'])].index)
    tup01, tup02 = scipy.stats.probplot(df[df[cat_feature] == feature_value[0]].Успешность, dist="norm")
    tup11, tup12 = scipy.stats.probplot(df[df[cat_feature] != feature_value[0]].Успешность, dist="norm")
    # for df[df[feature] == feature_value[0]:
    min_scale0 = math.floor(tup01[0][0])
    max_scale0 = math.ceil(tup01[0][-1])

    labels0 = list(range(min_scale0, max_scale0 + 1))
    line_data0 = []
    for i in range(len(labels0)):
        line_data0.append(tup02[0] * labels0[i] + tup02[1])
    label0 = f"Вероятность успешности по квантилям, где значение признака {cat_feature} равно {feature_value[0]}"
    qq_plot_data0 = []
    for i in range(len(tup01[0])):
        if i % 50 == 0:
            qq_plot_data0.append({"x": tup01[0][i], "y": tup01[1][i]})
    qq_plot_data0.append({"x": tup01[0][-1], "y": tup01[1][-1]})

    qq_chart_content0 = [labels0, line_data0, label0, qq_plot_data0]

    q_q_plot_to_json(qq_chart_content0, cat_feature.replace('(', '_').replace(')', '_').replace('/', '').replace(
        '.', '_').replace('-', '_').replace(' ', '_'))

    # for df[df[feature] != feature_value[0]:
    min_scale1 = math.floor(tup11[0][0])
    max_scale1 = math.ceil(tup11[0][-1])

    labels1 = list(range(min_scale1, max_scale1 + 1))
    line_data1 = []
    for i in range(len(labels1)):
        line_data1.append(tup12[0] * labels1[i] + tup12[1])
    label1 = f"Вероятность успешности по квантилям, где значение признака {cat_feature} не равно {feature_value[0]}"
    qq_plot_data1 = []
    for i in range(len(tup11[0])):
        if i % 50 == 0:
            qq_plot_data1.append({"x": tup11[0][i], "y": tup11[1][i]})
    qq_plot_data1.append({"x": tup11[0][-1], "y": tup11[1][-1]})

    qq_chart_content1 = [labels1, line_data1, label1, qq_plot_data1]

    q_q_plot_to_json(qq_chart_content1,
                     f'Не_{cat_feature}'.replace('(', '_').replace(')', '_').replace('/', '').replace(
                         '.', '_').replace('-', '_').replace(' ', '_'))


# catplot
def catplot_builder(df, cat_feature):
    data_grouped = df[[cat_feature, 'Успешность']].groupby(cat_feature).mean()
    labels = list(data_grouped.index)
    label = f"Catplot признака {cat_feature}"
    catplot_data = list(data_grouped.values)

    if str(type(catplot_data[0][0])) == "<class 'numpy.float64'>":
        catplot_data_np_dtype = copy.copy(catplot_data)
        catplot_data = []
        for dat in catplot_data_np_dtype:
            catplot_data.append(float(dat[0]))

    catplot_content = [labels, label, catplot_data]

    catplot_to_json(catplot_content, cat_feature.replace('(', '_').replace(')', '_').replace('/', '').replace(
        '.', '_').replace('-', '_').replace(' ', '_'))


# hypothises
def build_hypothises(df, feature):
    df_grouped = df[[feature, 'Успешность']].groupby(feature).mean()
    feature_value = list(df_grouped[df_grouped['Успешность'] == max(df_grouped['Успешность'])].index)
    if len(df[df[feature] == feature_value[0]]) < 3:
        return None, None, None, None, None, None
    qq_plot_builder(df, feature)
    w_statistic, p_value1 = scipy.stats.shapiro(df[df[feature] == feature_value[0]].Успешность)
    w_statistic, p_value2 = scipy.stats.shapiro(df[df[feature] != feature_value[0]].Успешность)
    if p_value1 < 0.01 or p_value2 < 0.01:
        statistic, pvalue = scipy.stats.ttest_ind(df[df[feature] == feature_value[0]].Успешность,
                                                  df[df[feature] != feature_value[0]].Успешность)
        i_norm = 0
    else:
        statistic, pvalue = scipy.stats.mannwhitneyu(df[df[feature] == feature_value[0]].Успешность,
                                                     df[df[feature] != feature_value[0]].Успешность)
        i_norm = 1
    catplot_builder(df, feature)
    return p_value1, p_value1, i_norm, pvalue, feature, feature_value[0]
