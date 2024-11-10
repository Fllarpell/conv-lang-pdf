from pdf_translator.pdf_rebuilder import create_translated_pdf
from pdf_translator.pdf_parser import extract_text_from_pdf


def process_pdf(file_path):
    extract_text_from_pdf(file_path, output_dir="/".join(file_path.split("/")[0:-2]) + "/output/extracted_text/")
    create_translated_pdf(file_path, "/".join(file_path.split("/")[0:-4]) + f"/media/data/output/{file_path.split('/')[-1]}")
    return "/".join(file_path.split("/")[0:-4]) + f"media/data/output/{file_path.split('/')[-1]}"
