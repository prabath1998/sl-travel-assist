import nltk
import numpy as np
from spellchecker import SpellChecker

from nltk.stem.porter import PorterStemmer
spell = SpellChecker()

nltk.download('punkt')

stemmer = PorterStemmer()

def autocorrect_tokens(tokens):
    return [spell.correction(word) for word in tokens]

def tokenize(sentence):
    words = nltk.word_tokenize(sentence)
    corrected_words = autocorrect_tokens(words)
    return corrected_words

def stem(word):
    if isinstance(word, str):
        return stemmer.stem(word.lower())
    return ""


def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1

    return bag