"""Module for the API."""

import pathlib

import random

from akshara import varnakaarya as vk


def get_random(filename: pathlib.Path = "data/words.csv") -> str:
    """Return a word from amarakosha."""

    with open(filename, "r", encoding="utf-8") as file:
        words = file.readlines()[0]

    word = random.choice(words.split(","))
    return word


def get_fixed_length(length: int, filename: pathlib.Path = "data/words.csv") -> str:
    """Return a word from amarakosha with a fixed length."""

    for _ in range(100):
        res = get_random(filename)

        try:
            akshaara = vk.get_akshara(res)
        except AssertionError:
            akshaara = []

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
        lines = file.readlines()[0]

    valid_words = lines.split(",")

    return word in valid_words
