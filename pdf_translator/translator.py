import openai
from transformers import MarianMTModel, MarianTokenizer


class Translator:
    def __init__(self, model_type="marian", model_name=None, openai_api_key=None):
        self.model_type = model_type

        if model_type == "marian":
            self.model_name = model_name or "Helsinki-NLP/opus-mt-en-ru"
            self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
            self.model = MarianMTModel.from_pretrained(self.model_name)
            self.max_length = 512
        elif model_type == "gpt4":
            if not openai_api_key:
                raise ValueError("API ключ OpenAI обязателен для использования GPT-4.")
            openai.api_key = openai_api_key
        else:
            raise ValueError("Unsupported model type. Use 'marian' or 'gpt4'.")

    def translate_text(self, text):
        if self.model_type == "marian":
            return self._translate_with_marian(text)
        elif self.model_type == "gpt4":
            return self._translate_with_gpt4(text)

    def _translate_with_marian(self, text):
        tokenized_text = self.tokenizer(
            text, return_tensors="pt", padding=True, truncation=True, max_length=self.max_length
        )
        translated = self.model.generate(**tokenized_text)
        return [self.tokenizer.decode(t, skip_special_tokens=True) for t in translated]

    def _translate_with_gpt4(self, text):
        prompt = f"Translate the following text to Russian:\n\n{text}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content'].strip()
