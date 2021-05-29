import copy
import itertools
import os

from django.http import HttpResponse
from django.shortcuts import render

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pylab as plb
import seaborn as sns
from scipy import stats
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, TableStyle, Table

CATEGORY_COLUMNS = ['Форма обучения', 'Квалификация', 'Курс', 'Специальность',
                    'Профиль', 'Выпуск. отдел.', 'Выпуск. школа', 'Группа',
                    'Обуч. подразд.', 'Форма финансирования', 'Страна', 'Гражданство',
                    'Пол', 'Дата рождения', 'Академ отпуск (действующий) - да / нет',
                    'Дисциплины по которым получены неудовлетворительные оценки', 'Курс', 'Класс']
NUMERIC_COLUMNS = ['Всего', 'Положительных', 'Неудовлетворительных',
                   'Пропусков по дисциплинам по которым получены неудовлетворительные оценки',
                   'Всего часов по дисциплинам по которым получены неудовлетворительные оценки',
                   'Всего часов пропусков в семестре', 'Всего часов аудиторных занятий в семестре', 'Успешность']

title_label = 6
figsize_width = 2.2
figsize_height = 1.4
x_label = 6
y_label = 6
xy_tick = 5


def dataset_report(request):
    filelist = os.listdir(path='uploads/datasets')
    processed_filelist = os.listdir(path='uploads/processed_datasets')
    return render(request, 'report_controller/dataset_report.html', {'filelist': filelist,
                                                   'processed_filelist': processed_filelist})


def report_result(request, file_path):
    response = pdf_report(f'uploads/datasets/{file_path}')
    return response


def processed_report_result(request, file_path):
    response = pdf_report(f'uploads/processed_datasets/{file_path}')
    return response


def addPageNumber(canvas, doc):
    page_num = canvas.getPageNumber()
    canvas.drawRightString(200 * mm, 10 * mm, str(page_num))


def pdf_report(dataset_filepath: str):
    plt.switch_backend('agg')
    df = pd.read_excel(dataset_filepath)
    df_cols = list(df.columns)
    if 'Курс' in df_cols:
        df['Курс'] = df['Курс'].astype('object')
    if 'Класс' in df_cols:
        df['Класс'] = df['Класс'].astype('object')
    cat_cols = []
    num_cols = []
    for col in df_cols:
        if col in CATEGORY_COLUMNS:
            cat_cols.append(col)
        elif col in NUMERIC_COLUMNS:
            num_cols.append(col)

    df_filename = dataset_filepath.split('/')[-1]
    df_name = ''
    string = df_filename.split('.')[:-1]
    for s in string:
        df_name += s
    pdf_filename = df_name + '_results.pdf'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s"' % pdf_filename

    pdfmetrics.registerFont(TTFont('Times', 'times.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('Times-Bold', 'timesbd.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('Times-Italic', 'timesi.ttf', 'UTF-8'))
    pdfmetrics.registerFont(TTFont('Times-BoldItalic', 'timesbi.ttf', 'UTF-8'))

    addMapping('Times', 0, 0, 'Times')  # normal
    addMapping('Times', 0, 1, 'Times-Italic')  # italic
    addMapping('Times', 1, 0, 'Times-Bold')  # bold
    addMapping('Times', 1, 1, 'Times-BoldItalic')  # italic and bold

    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=20, bottomMargin=40,
                            title='Результаты')
    story = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Times', fontSize=11))
    styles.add(ParagraphStyle(name='Justify-Bold', alignment=TA_JUSTIFY, fontName='Times-Bold'))
    bold_style = styles['Justify-Bold']
    normal_style = styles['Justify']
    doc_title = copy.copy(styles["Heading1"])
    doc_title.alignment = TA_LEFT
    doc_title.fontName = 'Times-Bold'
    doc_title.fontSize = 16
    logo = 'static/img/tpu-logo.png'
    im = Image(logo)
    story.append(im)
    story.append(Spacer(1, 10))
    title1 = "Статистика по характеристикам студентов за х семестр у года"
    story.append(Paragraph(title1, doc_title))

    result_table_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Times-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (15, -2), colors.lightgrey),
    ])

    normal_table_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Times', 10),
        ('ALIGN', (0, 0), (0, -1), 'CENTRE'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ])

    data = df_describe(df)
    table = Table(data)
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Times', 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))

    for col in df_cols:
        hist = df_hist(df, col, df_name)
        him = Image(hist)  # , 70 * mm, 40 * mm
        story.append(him)
        story.append(Spacer(1, 10))
        if col in num_cols:
            boxplot = df_boxplot(df, col, df_name)
            bim = Image(boxplot)  # , 70 * mm, 40 * mm
            story.append(bim)
            story.append(Spacer(1, 10))


    title2 = "Поиск скрытых зависимостей"
    story.append(Paragraph(title2, doc_title))
    doc_title.fontSize = 12

    for cat_col in cat_cols:
        title3 = cat_col
        story.append(Paragraph(title3, doc_title))

        catplot = df_catplot(df, cat_col, df_name)
        cim = Image(catplot)
        story.append(cim)
        story.append(Spacer(1, 10))

        qq_plot = df_qqplot(df, cat_col, df_name)
        qim = Image(qq_plot)
        story.append(qim)
        story.append(Spacer(1, 10))

        stats_str, result = df_hypothises(df, cat_col)
        story.append(Paragraph(stats_str, normal_style))
        for res in result:
            story.append(Paragraph(res, normal_style))
        story.append(Spacer(1, 10))

    doc.build(story, onFirstPage=addPageNumber, onLaterPages=addPageNumber)
    return response


def df_describe(df):
    df_desc = df.describe()
    df_desc_cols = ['']
    df_desc_cols += list(df_desc.columns)
    df_desc_idx = list(df_desc.index)
    data = []
    for i in range(len(df_desc_cols)):
        if len(df_desc_cols[i]) < 11:
            continue
        if len(df_desc_cols[i].split(' ')) == 1:
            continue
        c_inc = int(len(df_desc_cols[i]) / 2)
        c_decr = int(len(df_desc_cols[i]) / 2)
        while df_desc_cols[i][c_inc] != ' ' and df_desc_cols[i][c_decr] != ' ':
            if c_inc > len(df_desc_cols[i]):
                print(f"Переполнение c_inc: {c_inc}")
            if c_decr < 0:
                print(f"Переполнение c_decr: {c_decr}")
            c_inc += 1
            c_decr -= 1
        ch_list = []
        for ch in df_desc_cols[i]:
            ch_list.append(ch)
        if df_desc_cols[i][c_inc] == ' ':
            ch_list[c_inc] = '\n'
            df_desc_cols[i] = ''.join(ch_list)
        elif df_desc_cols[i][c_decr] == ' ':
            ch_list[c_decr] = '\n'
            df_desc_cols[i] = ''.join(ch_list)
    data.append(df_desc_cols)
    for i in range(len(df_desc)):
        tmp = [df_desc_idx[i]]
        for col in list(df_desc.columns):
            tmp.append(df_desc[col][i])
        data.append(tmp)
    return data


def df_hist(df, col, filename):
    path = f'static/img/hist'
    if not os.path.exists(path):
        os.mkdir(path)

    fig, ax = plt.subplots()
    if str(df[col].dtype) == 'object':
        val_cnt = df[col].value_counts()[:10]
        val_cnt_idx = list(val_cnt.index)
        val_cnt_vals = list(val_cnt.values)
        new_dict = {}
        for i in range(len(val_cnt)):
            if str(type(val_cnt_idx[i])) != "<class 'int'>" and len(val_cnt_idx[i]) > 30:
                val_cnt_idx[i] = ' '.join(val_cnt_idx[i].split(' ')[:5]) + '...'
            new_dict[val_cnt_idx[i]] = val_cnt_vals[i]
        ax.barh(list(reversed(list(new_dict.keys()))), list(reversed(list(new_dict.values()))))
        if len(list(df[col].unique())) > 10:
            ax.set_xlabel('Кол-во значений', fontsize=x_label)
            ax.set_ylabel('Топ 10 значений признака', fontsize=y_label)
        else:
            ax.set_xlabel('Кол-во значений', fontsize=x_label)
            ax.set_ylabel('Значения признака', fontsize=y_label)
    else:
        ax.hist(df[col])
        ax.set_xlabel('Значения признака', fontsize=x_label)
        ax.set_ylabel('Кол-во значений', fontsize=y_label)
    ax.set_title(col, fontsize=title_label)
    fig.set_figwidth(figsize_width)
    fig.set_figheight(figsize_height)
    plt.tick_params(axis='both', labelsize=xy_tick)

    col_repaired = ','.join(col.split('/'))
    hist_filepath = f"{path}/hist_{filename}_{col_repaired}.png"
    plt.savefig(hist_filepath, bbox_inches='tight')
    return hist_filepath


def df_boxplot(df, numeric_col, filename):
    path = f'static/img/boxplot'
    if not os.path.exists(path):
        os.mkdir(path)

    fig, ax = plt.subplots()
    ax.boxplot(df[numeric_col], vert=False, labels=[''])
    ax.set_title(numeric_col, fontsize=title_label)
    fig.set_figwidth(figsize_width)
    fig.set_figheight(figsize_height)
    plt.tick_params(axis='both', labelsize=xy_tick)

    boxplot_filepath = f"{path}/boxplot_{filename}_{numeric_col}.png"
    plt.savefig(boxplot_filepath, bbox_inches='tight')
    return boxplot_filepath


def df_catplot(df, cat_col, filename):
    path = f'static/img/catplot'
    if not os.path.exists(path):
        os.mkdir(path)

    if len(list(df[cat_col].unique())) > 5:
        df_grouped = df[[cat_col, 'Успешность']].groupby(cat_col).mean() \
            .sort_values(by='Успешность', ascending=False)
        feature_values = list(df_grouped[:4].index) + ['Все остальные']
        for i in range(len(feature_values)):
            if len(feature_values[i]) > 30:
                feature_values[i] = ' '.join(feature_values[i].split(' ')[:5]) + '...'
        feature_data = []
        for i in range(4):
            feature_data.append(df_grouped.values[i][0])
        feature_data.append(df_grouped[4:].mean().values[0])
        df_catplot_dat = pd.DataFrame({cat_col: feature_values, 'Успешность': feature_data})
        if cat_col in ['Профиль', 'Выпуск. отдел.', 'Обуч. подразд.', 'Гражданство']:
            g = sns.catplot(y=cat_col, x='Успешность', kind='point', data=df_catplot_dat, orient='h', height=3)
            g.ax.set_xlabel('Успешность', fontsize=x_label)
            g.ax.set_ylabel(cat_col, fontsize=y_label)
        else:
            g = sns.catplot(x=cat_col, y='Успешность', kind='point', data=df_catplot_dat)
            g.set_xticklabels(rotation=30)
            g.ax.set_xlabel(cat_col, fontsize=x_label)
            g.ax.set_ylabel('Успешность', fontsize=y_label)
    elif cat_col == 'Форма финансирования':
        g = sns.catplot(y=cat_col, x='Успешность', kind='point', data=df, orient='h', height=3)
        g.ax.set_xlabel('Успешность', fontsize=x_label)
        g.ax.set_ylabel(cat_col, fontsize=y_label)
    else:
        g = sns.catplot(x=cat_col, y='Успешность', kind='point', data=df)
        g.ax.set_xlabel(cat_col, fontsize=x_label)
        g.ax.set_ylabel('Успешность', fontsize=y_label)
    g.fig.set_figwidth(figsize_width)
    g.fig.set_figheight(figsize_height)
    plt.tick_params(axis='both', labelsize=xy_tick)

    col_repaired = ','.join(cat_col.split('/'))
    catplot_filepath = f"{path}/catplot_{filename}_{col_repaired}.png"
    g.savefig(catplot_filepath, bbox_inches='tight')
    return catplot_filepath


def df_qqplot(df, cat_col, filename):
    path = f'static/img/qq_plot'
    if not os.path.exists(path):
        os.mkdir(path)

    df_grouped = df[[cat_col, 'Успешность']].groupby(cat_col).mean()
    feature_value = list(df_grouped[df_grouped['Успешность'] == max(df_grouped['Успешность'])].index)[0]
    feat_name = feature_value
    if str(type(feature_value)) != "<class 'int'>" and len(feature_value) > 20:
        feat_name = feature_value.split(' ')[1] + '...' + feature_value.split(' ')[-1]
    plb.figure(figsize=(6, 4))
    ax1 = plb.subplot(2, 2, 1)
    stats.probplot(df[df[cat_col] == feature_value].Успешность, dist="norm", plot=plb)
    ax2 = plb.subplot(2, 2, 2)
    stats.probplot(df[df[cat_col] != feature_value].Успешность, dist="norm", plot=plb)

    ax1.set_title(f'Q-Q Plot значения {feat_name}', fontsize=title_label)
    ax1.set_xlabel('Теоретические квантили', fontsize=x_label)
    ax1.set_ylabel('Упорядоченные значения', fontsize=y_label)
    ax1.tick_params(axis='both', labelsize=xy_tick)

    ax2.set_title(f'Q-Q Plot значения не {feat_name}', fontsize=title_label)
    ax2.set_xlabel('Теоретические квантили', fontsize=x_label)
    ax2.set_ylabel('Упорядоченные значения', fontsize=y_label)
    ax2.tick_params(axis='both', labelsize=xy_tick)

    col_repaired = ','.join(cat_col.split('/'))
    qqplot_filepath = f"{path}/qq_plot_{filename}_{col_repaired}.png"
    plb.savefig(qqplot_filepath, bbox_inches='tight')
    return qqplot_filepath


def df_hypothises(df, col):
    df_grouped = df[[col, 'Успешность']].groupby(col).mean()
    feature_value = list(df_grouped[df_grouped['Успешность'] == max(df_grouped['Успешность'])].index)[0]

    if len(df[df[col] == feature_value]) < 3:
        p_value1 = -1
    else:
        _, p_value1 = stats.shapiro(df[df[col] == feature_value].Успешность)

    if len(df[df[col] != feature_value]) < 3:
        p_value2 = -1
    else:
        _, p_value2 = stats.shapiro(df[df[col] != feature_value].Успешность)

    stats_str = f"P-значение критерия Шапиро-Уилка равно: {p_value1} и {p_value2} соответственно."
    if p_value1 == -1 or p_value2 == -1:
        stats_str = "Недостаточно данных. Необходимо как минимум 3 значения"
        result = ['Для проведения статистических тестов не хватает данных']
    elif (0 < p_value1 <= 0.01) or (0 < p_value2 <= 0.01):
        _, pval = stats.ttest_ind(df[df[col] == feature_value].Успешность,
                                  df[df[col] != feature_value].Успешность)
        result = [f"Распределение нормальное. Использован t-критерий Стьюдента.",
                  f"P-значение t-критерия Стьюдента равно {pval}"]
        if pval > 0.01:
            result.append("Вывода по данному признаку сформировать не удалось.")
        else:
            result.append(f"Студенты, обладающие значением {feature_value} признака {col} обучаются успешнее.")
    else:
        _, pval1 = stats.mannwhitneyu(df[df[col] == feature_value].Успешность,
                                      df[df[col] != feature_value].Успешность)
        result = [f"Распределение ненормальное. Использован критерий Манна-Уитни.",
                  f"P-значение критерия Манна-Уитни равно {pval1}"]
        if pval1 > 0.01:
            result.append("Вывода по данному признаку сформировать не удалось.")
        else:
            result.append(f"Студенты, обладающие значением {feature_value} признака {col} обучаются успешнее.")

    return stats_str, result


def permutation_t_stat_ind(sample1, sample2):
    return np.mean(sample1) - np.mean(sample2)


def get_random_combinations(n1, n2, max_combinations):
    index = list(range(n1 + n2))
    indices = {tuple(index)}
    for i in range(max_combinations - 1):
        np.random.shuffle(index)
        indices.add(tuple(index))
    return [(index[:n1], index[n1:]) for index in indices]


def permutation_zero_dist_ind(sample1, sample2, max_combinations=None):
    joined_sample = np.hstack((sample1, sample2))
    n1 = len(sample1)
    n = len(joined_sample)

    if max_combinations:
        indices = get_random_combinations(n1, len(sample2), max_combinations)
    else:
        indices = [(list(index), filter(lambda i: i not in index, range(n)))
                   for index in itertools.combinations(range(n), n1)]

    distr = [joined_sample[list(i[0])].mean() - joined_sample[list(i[1])].mean() for i in indices]
    return distr


def permutation_test(sample, mean, max_permutations=None, alternative='two-sided'):
    if alternative not in ('two-sided', 'less', 'greater'):
        raise ValueError("alternative not recognized\n"
                         "should be 'two-sided', 'less' or 'greater'")
    t_stat = permutation_t_stat_ind(sample, mean)
    zero_distr = permutation_zero_dist_ind(sample, mean, max_permutations)
    if alternative == 'two-sided':
        return sum([1. if abs(x) >= abs(t_stat) else 0. for x in zero_distr]) / len(zero_distr)
    if alternative == 'less':
        return sum([1. if x <= t_stat else 0. for x in zero_distr]) / len(zero_distr)
    if alternative == 'greater':
        return sum([1. if x >= t_stat else 0. for x in zero_distr]) / len(zero_distr)
