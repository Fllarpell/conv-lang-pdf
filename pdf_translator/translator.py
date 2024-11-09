import fitz
import os
import logging
from transformers import MarianMTModel, MarianTokenizer


class TranslatorMarianMTModel:
    def __init__(self):
        self.model_name = "Helsinki-NLP/opus-mt-en-ru"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)
        self.max_length = 512

    def translate_text(self, text):
        # Разбиваем текст на блоки длиной не более max_length токенов
        tokenized_text = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=self.max_length)
        translated = self.model.generate(**tokenized_text)
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]