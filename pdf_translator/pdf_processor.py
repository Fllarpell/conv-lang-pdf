import fitz  # PyMuPDF
from PIL import Image


class PDFProcessor:
    def __init__(self, config):
        self.dpi = config.get("dpi", 300)

    def convert_pdf_to_images(self, pdf_path):
        images = []
        with fitz.open(pdf_path) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf[page_num]
                pix = page.get_pixmap(dpi=self.dpi)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                images.append(img)
        return images
