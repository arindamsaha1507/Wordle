"""Module to implement the Wordle game in Streamlit."""

import logging

import streamlit as st
from akshara import varnakaarya as vk
import yaml
from logtail import LogtailHandler

from evaluate import CellStatus, Compare
from word_processor import Word
from dictionary import get_fixed_length, get_synonyms
from grid import render_grid
from utils import (
    check_guess_word_length,
    is_guess_word_in_dictionary,
    select_geuss,
    transliteration_options,
    wait_for_guess_confirmation,
)

handler = LogtailHandler(source_token=st.secrets["LOGGING_TOKEN"])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)


WORD_LENGTH = 3
MAX_ATTEMPTS = 10

# Load the information about the game
with open("ui.yml", "r", encoding="utf-8") as file:
    all_text = yaml.safe_load(file)


helper_text = all_text["helper_text"]

if "true_word" not in st.session_state:

    info = get_fixed_length(WORD_LENGTH)
    logger.info("True word: %s", info["word"])

    st.session_state.true_word = Word(info["word"])

    st.session_state.shloka = info["shloka"].split("।")
    st.session_state.shloka[0] += "।"
    st.session_state.synonyms = get_synonyms(info["word"])
    st.session_state.message = ""
    st.session_state.valid_guess = None
    st.session_state.awaiting_guess = False
    st.session_state.current_row = 0
    st.session_state.guesses = [
        ["" for _ in range(WORD_LENGTH)] for _ in range(MAX_ATTEMPTS)
    ]
    st.session_state.guess_status = [
        [(CellStatus.ABSENT, CellStatus.ABSENT) for _ in range(WORD_LENGTH)]
        for _ in range(MAX_ATTEMPTS)
    ]
    st.session_state.game_over = False

    st.session_state.confirm_button_clicked = False
    st.session_state.options = []


true_word = st.session_state.true_word

# Main App Interface
st.title("Sanskrit Wordle")
st.write("Guess the Sanskrit word, one row at a time!")

with st.expander("How to Play"):
    st.write(
        "1. The word is a secret Sanskrit word from the Amarakosha having 3 Aksharas.\n\n"
        "2. Aksharas are a combination of Svaras and Vyanjanas.\n\n"
        "   - For example, मीनाक्षी has 3 Aksharas: मी, ना, क्षी\n"
        "   - मी = म् + ई. Here, म् is a Vyanjana and ई is a Svara.\n"
        "   - ना = न + आ. Here, न is a Vyanjana and आ is a Svara.\n"
        "   - क्षी = क् + ष् + ई. Here, क् and ष् are Vyanjanas and ई is a Svara.\n\n"
        "3. The grid will show the status of each Akshara in your guess.\n"
        "   - Green: Akshara is correct and in the right position.\n"
        "   - Orange: Akshara is correct but in the wrong position.\n"
        "   - Blue: Only the Svara is correct.\n"
        "   - Purple: At least one Vyanjana is correct.\n"
        "   - Red: Svara and one Vyanjana are correct, but the Akshara is incorrect.\n\n"
        "4. You have 10 attempts to guess the word.\n\n"
        "5. If you guess the word correctly, you win!\n\n"
        "6. If you run out of attempts, the game is over.\n\n"
        "7. You can enter your guesses in Romanized Sanskrit or Devanagari script."
    )


render_grid(WORD_LENGTH, MAX_ATTEMPTS, helper_text)

if not st.session_state.game_over:

    guess = st.text_input("Enter your guess:")

    if st.button("Submit Guess"):
        try:
            vk.get_akshara(guess)
            st.session_state.valid_guess = guess
        except AssertionError:

            transliteration_options(guess)
            wait_for_guess_confirmation()

    if st.session_state.awaiting_guess:
        select_geuss()

    if st.session_state.valid_guess and not st.session_state.awaiting_guess:
        guess_word = Word(st.session_state.valid_guess)

        check_guess_word_length(guess_word, WORD_LENGTH)
        is_guess_word_in_dictionary(guess_word)

        logger.info("Guess word: %s for True word: %s", guess_word.word, true_word.word)

        compare = Compare(true_word, guess_word)
        compare.compare()
        st.session_state.guess_status[st.session_state.current_row] = compare.status
        st.session_state.guesses[st.session_state.current_row] = guess_word.aksharas
        st.session_state.current_row += 1

        if compare.status == [(CellStatus.CORRECT, CellStatus.CORRECT)] * WORD_LENGTH:
            st.session_state.message += f"Congratulations! You have guessed the word correctly. Score: {MAX_ATTEMPTS - st.session_state.current_row + 1} / 10.\n"
            st.session_state.game_over = True
            logger.info(
                "Score: %s for True Word: %s",
                MAX_ATTEMPTS - st.session_state.current_row + 1,
                true_word.word,
            )

        if st.session_state.current_row == MAX_ATTEMPTS:
            st.session_state.game_over = True
            logger.info(
                "Score: %s for True Word: %s",
                MAX_ATTEMPTS - st.session_state.current_row + 1,
                true_word.word,
            )

        if st.session_state.game_over:
            st.session_state.message += f"## The word was {true_word.word}.\n"
            st.session_state.message += " The shloka is: \n"
            st.session_state.message += f"### {st.session_state.shloka[0]}\n"
            st.session_state.message += f"### {st.session_state.shloka[1]}\n"
            st.session_state.message += "## Synonyms\n"
            st.session_state.message += ", ".join(st.session_state.synonyms["synonyms"])

        st.session_state.valid_guess = None  # Reset the valid guess for next input
        st.rerun()

if st.session_state.game_over:
    st.success(st.session_state.message)

    if st.button("Play Again"):
        st.session_state.clear()
        st.rerun()

st.write("---")

with st.expander(
    "Liked the app? Checkout some of the other Sanskrit related projects we have been working on!"
):
    st.write(
        "1. [सङ्ख्याकारः](https://sankhya.streamlit.app/) - A Sanskrit number converter that converts numbers to words.\n"
        "2. [अक्षर](https://pypi.org/project/akshara/) - A Python library for working with Sanskrit Varnas.\n"
        "3. [वाक्यसन्धि](https://sandhi.streamlit.app/) - An app that performs Sanskrit Sandhi sentences (still in development).\n"
    )
