import pytesseract
import cv2
import numpy as np
from typing import List, Dict
from pdf_translator.utils import draw_bounding_boxes

class TextClassifier:
    def __init__(self):
        self.ocr_config = "--oem 1 --psm 6"  # Режимы OCR для улучшенного распознавания текста

    def classify_and_extract_text_blocks(self, image) -> List[Dict]:
        """
        Основной метод для классификации блоков на изображении.
        Возвращает список блоков с координатами, содержимым и типом.
        """
        # Шаг 1: Извлечение текста и координат блоков с помощью OCR
        raw_blocks = self._extract_text_blocks(image)

        # Шаг 2: Классификация блоков по типу
        classified_blocks = []
        for block in raw_blocks:
            classified_block = self._classify_block(block)
            classified_blocks.append(classified_block)

        return classified_blocks

    def _extract_text_blocks(self, image) -> List[Dict]:
        """
        Извлечение текстовых блоков с использованием OCR.
        Возвращает список словарей с текстом и координатами каждого блока.
        """
        # Преобразуем изображение в ч/б для улучшения OCR
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        _, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

        # Применяем OCR для извлечения текста и координат
        ocr_data = pytesseract.image_to_data(binary_image, config=self.ocr_config, output_type=pytesseract.Output.DICT)

        text_blocks = []
        num_blocks = len(ocr_data["text"])
        for i in range(num_blocks):
            if int(ocr_data["conf"][i]) > 60:  # Фильтруем блоки с низкой уверенностью
                block = {
                    "text": ocr_data["text"][i],
                    "left": ocr_data["left"][i],
                    "top": ocr_data["top"][i],
                    "width": ocr_data["width"][i],
                    "height": ocr_data["height"][i],
                }
                text_blocks.append(block)

        return text_blocks

    def _classify_block(self, block: Dict) -> Dict:
        """
        Классификация блока по типу на основе содержимого и координат.
        Обновляет словарь блока, добавляя тип блока (text, title, footnote, image).
        """
        # Простые правила классификации по длине текста и размеру блока
        text_length = len(block["text"])

        if text_length > 100:
            block["type"] = "text"
        elif text_length < 20 and block["height"] > 15:
            block["type"] = "title"
        elif "footnote" in block["text"].lower():
            block["type"] = "footnote"
        else:
            block["type"] = "text"  # По умолчанию считаем текстом

        return block

    def _extract_images(self, image) -> List[Dict]:
        """
        Извлечение изображений и таблиц из документа с использованием OpenCV.
        Определяет области, которые не содержат текста, но выглядят как графика.
        """
        # Преобразование в серый и бинаризация
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        _, binary_image = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY_INV)

        # Определение контуров возможных изображений
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        images = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if area > 5000:  # Порог по площади, чтобы избежать мелких деталей
                images.append({
                    "left": x,
                    "top": y,
                    "width": w,
                    "height": h,
                    "type": "image"
                })

        return images

    def classify_content(self, image) -> List[Dict]:
        """
        Классифицирует все блоки на изображении, включая текстовые и графические элементы.
        Возвращает список блоков с типами и координатами.
        """
        # Извлекаем текстовые и графические блоки
        text_blocks = self.classify_and_extract_text_blocks(image)
        image_blocks = self._extract_images(image)

        # Объединяем текстовые и графические блоки
        all_blocks = text_blocks + image_blocks
        return sorted(all_blocks, key=lambda x: (x["top"], x["left"]))  # Сортируем для последовательности
