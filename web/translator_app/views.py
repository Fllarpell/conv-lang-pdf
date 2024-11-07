from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import UploadFileForm
from pdf_translator.processor import process_pdf  # Импорт функции для перевода
import os

def translate_pdf(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = default_storage.save(f"{file.name}", file)

            # Запуск процесса перевода
            output_path = process_pdf(file_path)  # output_path - это путь к сохраненному файлу

            # Формируем URL для скачивания файла
            file_name = os.path.basename(output_path)
            output_url = f"{settings.MEDIA_URL}{file_name}"

            return render(request, 'translator_app/result.html', {
                'output_url': output_url
            })
    else:
        form = UploadFileForm()

    return render(request, 'translator_app/upload.html', {'form': form})
