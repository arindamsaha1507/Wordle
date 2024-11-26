"""Utility functions for the project."""

import time
import streamlit as st

from google.transliteration import transliterate_word

from dictionary import is_word_in_dictionary
from word_processor import Word


def transliteration_options(word: str) -> None:
    """Transliterate a word from one script to another."""

    st.session_state.options = transliterate_word(word, lang_code="sa")


def wait_for_guess_confirmation() -> None:
    """Wait for the user to confirm their guess."""

    if not st.session_state.awaiting_guess:
        st.session_state.valid_guess = None
        st.session_state.awaiting_guess = True
        st.session_state.confirm_button_clicked = False


def select_geuss() -> None:
    """Select the correct guess from the options."""

    dialogue = "Select the correct option:"
    selected_guess = st.selectbox(dialogue, st.session_state.options)
    if st.button("Confirm Guess", key="confirm_guess_button"):
        st.session_state.valid_guess = selected_guess
        st.session_state.awaiting_guess = False
        st.session_state.confirm_button_clicked = True  # Mark button as clicked
        st.rerun()  # Force rerun to process confirmed guess


def check_guess_word_length(guess_word: Word, word_length: int) -> None:
    """Check if the word is of the correct length."""

    if len(guess_word.aksharas) != word_length:

        message = "Invalid guess! "
        message += f"Your guess has {len(guess_word.aksharas)} Aksharas. "
        message += f"Please guess a word with {word_length} Aksharas."
        st.error(message)
        st.session_state.valid_guess = None

        time.sleep(5)

        st.rerun()


def is_guess_word_in_dictionary(guess_word: Word) -> None:
    """Check if the word is in the dictionary."""

    if not is_word_in_dictionary(guess_word.word):
        st.error(
            f"Invalid guess! The word {guess_word.word} is not in the amarakosha dictionary."
        )
        st.session_state.valid_guess = None

        time.sleep(5)

        st.rerun()


def is_word_previously_guessed(guess_word: Word) -> None:
    """Check if the word has been previously guessed."""

    if guess_word.word in st.session_state.previous_guesses:
        st.error(f"Invalid guess! The word {guess_word.word} has already been guessed.")
        st.session_state.valid_guess = None

        time.sleep(5)

        st.rerun()
