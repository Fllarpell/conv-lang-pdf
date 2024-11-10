from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import UploadFileForm
import os
from pathlib import Path
from django.shortcuts import redirect

from pdf_translator.processor import process_pdf

output_url = ""


def download_pdf(request):
    return render(request, 'translator_app/result.html', {
        'output_url': output_url
    })


def translate_pdf(request):
    global output_url

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            default_storage.save(f"{Path(__file__).resolve().parent.parent}/media/data/input/{file.name}", file)
            output_path = process_pdf(f"{Path(__file__).resolve().parent.parent}/media/data/input/{file.name}")

            output_url = settings.MEDIA_URL + f"data/output/{os.path.basename(output_path)}"

            return redirect('/translate/download')

    else:
        form = UploadFileForm()

    return render(request, 'translator_app/upload.html', {'form': form})
