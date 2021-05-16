import os
from django import forms

PREP_FILE_CHOICES = []


def file_choice_update(path, filename):
    x = globals()
    x[filename] = []
    tmp = os.listdir(path=path)
    inc = 1
    for el in tmp:
        x[filename].append((inc, el))
        inc += 1
    print('func applied')
    print(x[filename])


file_choice_update('uploads/datasets_prepared', 'PREP_FILE_CHOICES')


class MLModelForm(forms.Form):
    prep_file_name = forms.ChoiceField(choices=PREP_FILE_CHOICES, widget=forms.RadioSelect)
