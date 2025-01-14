import os
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk import download

class TextCleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.translate(str.maketrans('', '', string.digits))
        words = word_tokenize(text)
        return [word.lower() for word in words if word.lower() not in self.stop_words]

    def process_documents(self, file_path):
        word_counter = Counter()

        if os.path.isfile(file_path) and file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                words = self.clean_text(content)
                word_counter.update(words)
        else:
            raise ValueError
        return word_counter

