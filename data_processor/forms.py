import os

from django import forms

import pandas as pd


class DataProcessForm(forms.Form):
    def __init__(self, file_name, *args, **kwargs):
        super(DataProcessForm, self).__init__(*args, **kwargs)
        df = pd.read_excel(f"uploads/datasets/{file_name}")
        hand_not_inf_choices = zip(df.columns, df.columns)
        self.fields['hand_not_inf'] = forms.MultipleChoiceField(choices=hand_not_inf_choices,
                                                                widget=forms.CheckboxSelectMultiple(
                                                                    attrs={"class": "checkbox dataprocess_radio"}))

    missing_choices = [("Заменить медианой признака для числовых, категорией "
                        "\"Нет\" для категориальных признаков", "Заменить медианой признака для числовых, категорией "
                                                                "\"Нет\" для категориальных признаков"),
                       ("Удалить запись с миссингом", "Удалить запись с миссингом"),
                       ("Не обрабатывать миссинги", "Не обрабатывать миссинги")]
    outlayers_choices = [("Удалить записи с выбросом", "Удалить записи с выбросом"),
                         ("Не обрабатывать записи с выбросами", "Не обрабатывать записи с выбросами")]
    linear_dep_choices = [("Исключить линейные зависимости", "Исключить линейные зависимости"),
                          ("Не исключать линейные зависимости", "Не исключать линейные зависимости")]
    target_val_choices = [("Сформировать целевые переменные", "Сформировать целевые переменные"),
                          ("Не формировать целевые переменные", "Не формировать целевые переменные")]
    facult_choices = [("Удалить факультативы", "Удалить факультативы"),
                      ("Не удалять факультативы", "Не удалять факультативы")]
    not_inf_choices = [("Обработать неинформативные признаки", "Обработать неинформативные признаки"),
                       ("Не обрабатывать неинформативные признаки", "Не обрабатывать неинформативные признаки")]
    missing = forms.ChoiceField(choices=missing_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio"}))
    outlayers = forms.ChoiceField(choices=outlayers_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio"}))
    linear_dep = forms.ChoiceField(choices=linear_dep_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio"}))
    target_val = forms.ChoiceField(choices=target_val_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio"}))
    facult = forms.ChoiceField(choices=facult_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio"}))
    not_inf = forms.ChoiceField(choices=not_inf_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio"}))


class DatasetForm(forms.Form):
    dataset_list = os.listdir(path='uploads/datasets')
    dataset_choices = zip(dataset_list, dataset_list)

    dataset = forms.ChoiceField(choices=dataset_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio todo-list"}))
