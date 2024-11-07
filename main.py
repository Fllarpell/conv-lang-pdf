from pdf_translator.pdf_processor import PDFProcessor
from pdf_translator.text_classifier import TextClassifier
from pdf_translator.translator import TranslatorMarianMTModel
from pdf_translator.pdf_rebuilder import create_translated_pdf
from pdf_translator.pdf_parser import extract_text_from_pdf
import yaml
import os

with open("config/development.yaml", "r") as f:
    config = yaml.safe_load(f)


def main():
    extract_text_from_pdf("data/input/input.pdf")
    create_translated_pdf("data/input/input.pdf", "data/output/output.pdf")

    # def sort_files(file_list):
    #     return sorted(file_list, key=lambda x: (int(x.split('_')[1].split(".")[0])))
    #
    # for _, _, files in os.walk("data/output/extracted_text"):
    #     file_dir = sort_files(files)
    #     source_text = []
    #     for file in file_dir:
    #         source_text.clear()
    #         text = ""
    #
    #
    #         with open("data/output/extracted_text/" + file, "r") as f:
    #             for line in f.readlines():
    #                 text += line
    #             source_text.append(text)
    #         try:
    #             translated = translator.translate_text(source_text)
    #         except IndexError:
    #             continue

if __name__ == "__main__":
    main()
