import os

from django.shortcuts import render
from .forms import UploadFileForm

import pandas as pd


def preview_df(df):
    return df.iloc[1:11].values, list(df.columns)


def dataset(request, file_path):
    df = pd.read_excel(f'uploads/datasets/{file_path}')
    first_rows, col_names = preview_df(df)
    return render(request, 'data_loader/dataset.html', {'first_rows': first_rows, 'col_names': col_names})

def processed_dataset(request, file_path):
    df = pd.read_excel(f'uploads/processed_datasets/{file_path}')
    first_rows, col_names = preview_df(df)
    return render(request, 'data_loader/dataset.html', {'first_rows': first_rows, 'col_names': col_names})

def filelist(request):
    filelist = os.listdir(path='uploads/datasets')
    processed_filelist = os.listdir(path='uploads/processed_datasets')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return render(request, 'data_loader/filelist.html', {'form': form, 'filelist': filelist,
                                                     'processed_filelist': processed_filelist})
    else:
        form = UploadFileForm
    return render(request, 'data_loader/filelist.html', {'form': form, 'filelist': filelist,
                                             'processed_filelist': processed_filelist})


def handle_uploaded_file(f):
    title = f.name
    with open(f'uploads/datasets/{title}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
