import fitz
import logging
import nltk
from nltk.tokenize import sent_tokenize
from pdf_translator.translator import Translator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/debug.log"),
        logging.StreamHandler()
    ]
)

nltk.download('punkt')
nltk.download('punkt_tab')


def create_translated_pdf(input_pdf_path, output_pdf_path):
    logging.info(f"Starting translation and PDF creation at: {output_pdf_path}")
    translateModel = Translator()

    document = fitz.open(input_pdf_path)
    translated_document = fitz.open()

    for page_num in range(document.page_count):
        page = document[page_num]
        translated_page = translated_document.new_page(width=page.rect.width, height=page.rect.height)
        font = fitz.Font("tiro")
        translated_page.insert_font(fontname="F0", fontbuffer=font.buffer)

        blocks = page.get_text("blocks")

        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]

            img_rect = page.get_image_rects(xref)[0]
            translated_page.insert_image(
                img_rect,
                stream=image_bytes,
                keep_proportion=True
            )

        for block in blocks:
            x0, y0, x1, y1, text, _, _ = block

            sentences = sent_tokenize(text)
            translated_text = ""

            for i in range(0, len(sentences), 1):
                chunk = ' '.join(sentences[i:i + 1])
                if chunk:
                    try:
                        translated_chunk = translateModel.translate_text([chunk])[0]
                        translated_text += translated_chunk + " "
                    except IndexError:
                        continue

            translated_page.insert_textbox(
                fitz.Rect(x0, y0, x1, y1),
                translated_text.strip(),
                fontsize=10,
                fontname="F0",
                align=0
            )

    translated_document.save(output_pdf_path)
    translated_document.close()
    document.close()
    logging.info(f"Translated PDF saved at: {output_pdf_path}")
