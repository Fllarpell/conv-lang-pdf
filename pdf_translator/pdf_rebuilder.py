import fitz
import os
import logging

from pdf_translator.translator import TranslatorMarianMTModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/debug.log"),
        logging.StreamHandler()
    ]
)


def create_translated_pdf(input_pdf_path, output_pdf_path):
    logging.info(f"Начат перевода и создание нового PDF файла по пути: {output_pdf_path}")
    translateModel = TranslatorMarianMTModel()

    document = fitz.open(input_pdf_path)
    translated_document = fitz.open()
    cnt = 0
    for page_num in range(document.page_count):
        cnt += 1
        if cnt % 20 == 0:
            logging.info(f"Переведено: {cnt/document.page_count * 100}% исходного файла")
        page = document[page_num]
        translated_page = translated_document.new_page(width=page.rect.width, height=page.rect.height)
        blocks = page.get_text("blocks")

        for block in blocks:
            x0, y0, x1, y1, text, _, _ = block
            try:
                translated_text = translateModel.translate_text([text])[0]
            except IndexError:
                continue
            translated_page.insert_textbox(
                fitz.Rect(x0, y0, x1, y1),
                translated_text,
                fontsize=10,
                fontname="helv",
                align=0
            )

    translated_document.save(output_pdf_path)
    translated_document.close()
    document.close()
    logging.info(f"Переведенный PDF сохранен по пути: {output_pdf_path}")


