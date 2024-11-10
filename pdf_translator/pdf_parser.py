import fitz
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/debug.log"),
        logging.StreamHandler()
    ]
)


def extract_text_from_pdf(pdf_path, output_dir="data/output/extracted_text"):
    os.makedirs(output_dir, exist_ok=True)

    document = fitz.open(pdf_path)
    logging.info(f"Начато извлечение текста из файла: {pdf_path}")
    cnt = 0
    for page_num in range(document.page_count):
        cnt += 1
        page = document[page_num]
        blocks = page.get_text("blocks")

        extracted_text_on_page = ""
        for block_num, block in enumerate(blocks):
            x0, y0, x1, y1, text, _, _, = block

            words_in_text = text.split(" ")
            for word in text.split(" "):
                if "-\n" in word:
                    transfer_word = "\n" + word.split("-\n")[0] + word.split("-\n")[1]
                    words_in_text[words_in_text.index(word)] = transfer_word

            text = " ".join(words_in_text)

            extracted_text_on_page += text

        block_file_path = os.path.join(output_dir, f"page_{page_num + 1}.txt")
        with open(block_file_path, "w", encoding="utf-8") as f:
            f.write(extracted_text_on_page)

    document.close()
    logging.info("Извлечение текста завершено!")
