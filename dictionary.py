"""Module for the API."""

import random

from akshara import varnakaarya as vk


def get_random():
    """Return a word from amarakosha."""

    with open("data/words.csv", "r", encoding="utf-8") as file:
        words = file.readlines()

    with open("data/shlokas.csv", "r", encoding="utf-8") as file:
        shlokas = file.readlines()

    line = words[random.choice(range(len(words)))]
    word = line.split(",")[0]
    linga = line.split(",")[1]
    shloka_number = line.split(",")[2]

    shloka = [line for line in shlokas if shloka_number in line][0].split(",")[0]

    return {"word": word, "linga": linga, "shloka": shloka}


def get_fixed_length(length: int):
    """Return a word from amarakosha with a fixed length."""

    for _ in range(100):
        res = get_random()
        akshaara = vk.get_akshara(res["word"])

        if len(akshaara) == length and "ं" not in akshaara:
            return res

    return {"error": "No word found with the given length."}


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
