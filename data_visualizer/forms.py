import os

from django import forms


class DatasetForm(forms.Form):
    dataset_list = os.listdir(path='uploads/datasets')
    processed_dataset_list = os.listdir(path='uploads/processed_datasets')
    dataset_choices = zip(dataset_list, dataset_list)
    processed_dataset_choices = zip(processed_dataset_list, processed_dataset_list)

    dataset = forms.ChoiceField(choices=dataset_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio"}))
    processed_dataset = forms.ChoiceField(choices=processed_dataset_choices, widget=forms.RadioSelect(
        attrs={"class": "radio dataprocess_radio"}))
