"""Module for the API."""

import random

from akshara import varnakaarya as vk


def get_random() -> str:
    """Return a word from amarakosha."""

    with open("data/words.csv", "r", encoding="utf-8") as file:
        words = file.readlines()

    line = words[random.choice(range(len(words)))]
    word = line.split(",")[0]

    return word


def get_fixed_length(length: int) -> str:
    """Return a word from amarakosha with a fixed length."""

    for _ in range(100):
        res = get_random()
        akshaara = vk.get_akshara(res)

        if len(akshaara) == length:
            return res

    return None


def get_synonyms(word: str):
    """Return the synonyms of a word."""

    with open("data/synonyms.csv", "r", encoding="utf-8") as file:
        synonyms = file.readlines()

    for line in synonyms:
        if word in line:
            return {"synonyms": line.split(",")[2].split()}

    return {"error": "No synonyms found for the given word."}


def is_word_in_dictionary(word: str):
    """Check if the given word is in the dictionary."""

    with open("data/words.csv", "r", encoding="utf-8") as file:
        lines = file.readlines()

    valid_words = [line.split(",")[0] for line in lines]

    return word in valid_words
