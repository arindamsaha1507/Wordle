"""Module to implement the Wordle game in Streamlit."""

import time
import streamlit as st
from google.transliteration import transliterate_word
from akshara import varnakaarya as vk

from evaluate import CellStatus, Compare
from word_processor import Word
from dictionary import get_fixed_length, get_synonyms


INFO = [
    "### Key",
    "<div style='background-color: green; width: 20px; height: 20px; display: inline-block;'></div> Akshara is present in the word and in the right position",
    "<div style='background-color: orange; width: 20px; height: 20px; display: inline-block;'></div> Akshara is present in the word but in the wrong position",
    "<div style='background-color: blue; width: 20px; height: 20px; display: inline-block;'></div> Only the Svara is present in the word",
    "<div style='background-color: purple; width: 20px; height: 20px; display: inline-block;'></div> At least one Vyanjana is present in the word",
    "<div style='background-color: red; width: 20px; height: 20px; display: inline-block;'></div> Svara and atleast one Vyanjana are present in thw word, but the Akshara is not",
    "",
    "",
    "",
    "",
]


if "true_word" not in st.session_state:
    info = get_fixed_length(3)
    st.session_state.true_word = Word(info["word"])
    st.session_state.shloka = info["shloka"].split("।")
    st.session_state.shloka[0] += "।"
    st.session_state.synonyms = get_synonyms(info["word"])
    st.session_state.message = ""
    st.session_state.valid_guess = None
    st.session_state.awaiting_guess = False


true_word = st.session_state.true_word
word_length = len(true_word.aksharas)
max_attempts = 10

col_widths = [2 / word_length for _ in range(word_length)]
col_widths.append(0.1)
col_widths.append(4)

col_widths = [width / sum(col_widths) for width in col_widths]

# Define global variables for the game
if "current_row" not in st.session_state:
    st.session_state.current_row = 0
if "guesses" not in st.session_state:
    st.session_state.guesses = [
        ["" for _ in range(word_length)] for _ in range(max_attempts)
    ]
if "guess_status" not in st.session_state:
    st.session_state.guess_status = [
        [CellStatus.ABSENT for _ in range(word_length)] for _ in range(max_attempts)
    ]
if "game_over" not in st.session_state:
    st.session_state.game_over = False


cell_colors_dict = {
    CellStatus.CORRECT: "green",
    CellStatus.PRESENT: "orange",
    CellStatus.ABSENT: "gray",
    CellStatus.SVARA_ONLY: "blue",
    CellStatus.VYANJANA_ONLY: "purple",
    CellStatus.SVARA_AND_VYANJANA: "red",
}


def grid_cell_markdown(akshara: str, status: CellStatus) -> str:
    """Return the HTML for a grid cell."""

    cell_color = cell_colors_dict[status]
    return f"<div style='text-align: center; background-color: {cell_color}; color: white; height: 50px; line-height: 50px; margin-bottom: 10px;'>{akshara}</div>"


# Render the Grid
def render_grid():
    """Render the grid of Aksharas."""

    for row in range(max_attempts):
        cols = st.columns(spec=col_widths, gap="small")
        for col_idx, col in enumerate(cols):

            if col_idx < word_length:
                akshara = st.session_state.guesses[row][col_idx]
                status = st.session_state.guess_status[row][col_idx]
                col.markdown(
                    grid_cell_markdown(akshara, status), unsafe_allow_html=True
                )

            elif col_idx == word_length + 1:
                col.markdown(INFO[row], unsafe_allow_html=True)


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


render_grid()

if not st.session_state.game_over:
    guess = st.text_input("Enter your guess:")

    # Ensure session state variables for managing guess and confirmation are initialized
    if "valid_guess" not in st.session_state:
        st.session_state.valid_guess = None
    if "awaiting_guess" not in st.session_state:
        st.session_state.awaiting_guess = False
    if "confirm_button_clicked" not in st.session_state:
        st.session_state.confirm_button_clicked = False
    if "options" not in st.session_state:
        st.session_state.options = []

    if st.button("Submit Guess"):
        try:
            vk.get_akshara(guess)
            st.session_state.valid_guess = guess
        except AssertionError:
            # options = transliterate_word(guess, lang_code="sa")
            st.session_state.options = transliterate_word(guess, lang_code="sa")
            # guess = st.selectbox("Select the correct option:", options)

            if not st.session_state.awaiting_guess:
                st.session_state.valid_guess = None
                st.session_state.awaiting_guess = True
                st.session_state.confirm_button_clicked = (
                    False  # Reset confirm button state
                )

    if st.session_state.awaiting_guess:
        selected_guess = st.selectbox(
            "Select the correct option:", st.session_state.options
        )
        if st.button("Confirm Guess", key="confirm_guess_button"):
            st.session_state.valid_guess = selected_guess
            st.session_state.awaiting_guess = False
            st.session_state.confirm_button_clicked = True  # Mark button as clicked
            st.rerun()  # Force rerun to process confirmed guess

    if st.session_state.valid_guess and not st.session_state.awaiting_guess:
        guess_word = Word(st.session_state.valid_guess)

        if len(guess_word.aksharas) != word_length:
            st.error(
                f"Invalid guess! Your guess has {len(guess_word.aksharas)} Aksharas. Please guess a word with {word_length} Aksharas."
            )
            st.session_state.valid_guess = None

            time.sleep(5)

            st.rerun()

        compare = Compare(true_word, guess_word)
        compare.compare()
        st.session_state.guess_status[st.session_state.current_row] = compare.status
        st.session_state.guesses[st.session_state.current_row] = guess_word.aksharas
        st.session_state.current_row += 1

        if compare.status == [CellStatus.CORRECT] * word_length:
            st.session_state.message += (
                "Congratulations! You have guessed the word correctly.\n"
            )
            st.session_state.game_over = True

        if st.session_state.current_row == max_attempts:
            st.session_state.game_over = True

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
        info = get_fixed_length(3)
        st.session_state.true_word = Word(info["word"])
        st.session_state.shloka = info["shloka"].split("।")
        st.session_state.shloka[0] += "।"
        st.session_state.synonyms = get_synonyms(info["word"])
        st.session_state.message = ""
        st.session_state.valid_guess = None
        st.session_state.awaiting_guess = False
        st.session_state.current_row = 0
        st.session_state.guesses = [
            ["" for _ in range(word_length)] for _ in range(max_attempts)
        ]
        st.session_state.guess_status = [
            [CellStatus.ABSENT for _ in range(word_length)] for _ in range(max_attempts)
        ]
        st.session_state.game_over = False
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
