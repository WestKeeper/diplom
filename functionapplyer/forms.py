import os
from django import forms


RAW_FILE_CHOICES = []
PREP_FILE_CHOICES = []
FUNC_CHOICES = (
    (1, 'encode_personal_data'),
    (2, 'drop_unnecessary_cols'),
    (3, 'delete_extra_disciplines'),
    (4, 'delete_linear_dependencies'),
    (5, 'clean_outliers'),
    (6, 'clean_missings_dropna'),
    (7, 'clean_missings_fillna'),
    (8, 'reformat_cols_type'),
    (9, 'create_target_vars')
)


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


file_choice_update('uploads/datasets', 'RAW_FILE_CHOICES')
file_choice_update('uploads/datasets_prepared', 'PREP_FILE_CHOICES')


def filestorage_update_activator():
    file_choice_update('uploads/datasets', 'RAW_FILE_CHOICES')
    file_choice_update('uploads/datasets_prepared', 'PREP_FILE_CHOICES')
    print('updated')


class FuncFileNameForm(forms.Form):
    raw_file_name = forms.ChoiceField(choices=RAW_FILE_CHOICES, required=False, widget=forms.RadioSelect)
    prep_file_name = forms.ChoiceField(choices=PREP_FILE_CHOICES, required=False, widget=forms.RadioSelect)
    func_name = forms.MultipleChoiceField(choices=FUNC_CHOICES, widget=forms.CheckboxSelectMultiple)

    def set_raw_file_name(self, value):
        self.raw_file_name = forms.ChoiceField(choices=value, required=False, widget=forms.RadioSelect)
        print('raw installed')

    def set_prep_file_name(self, value):
        self.prep_file_name = forms.ChoiceField(choices=value, required=False, widget=forms.RadioSelect)
        print('prep installed')
