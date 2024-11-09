from pdf_translator.pdf_rebuilder import create_translated_pdf
from pdf_translator.pdf_parser import extract_text_from_pdf


def main():
    #extract_text_from_pdf("data/input/input.pdf")
    create_translated_pdf("data/input/input.pdf", "data/output/output.pdf")


if __name__ == "__main__":
    main()
