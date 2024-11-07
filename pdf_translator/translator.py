from transformers import pipeline
from transformers import MarianMTModel, MarianTokenizer


class TranslatorMarianMTModel:
    def __init__(self):
        self.model_name = "Helsinki-NLP/opus-mt-en-ru"
        self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
        self.model = MarianMTModel.from_pretrained(self.model_name)

    def translate_text(self, text):
        translated = self.model.generate(**self.tokenizer(text, return_tensors="pt", padding=True))
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]

