import logging
import cv2
import numpy as np
from PIL import Image


def setup_logging(log_path):
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger()


def draw_bounding_boxes(image, blocks):
    """
    Вспомогательная функция для отрисовки прямоугольников вокруг блоков.
    """
    img_copy = np.array(image.copy())
    for block in blocks:
        x, y, w, h = block["left"], block["top"], block["width"], block["height"]
        color = (0, 255, 0) if block["type"] == "text" else (0, 0, 255)
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img_copy, block["type"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return Image.fromarray(img_copy)
