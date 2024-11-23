"""Module to implement the Wordle game in Streamlit."""

import streamlit as st

from evaluate import CellStatus, Compare
from word_processor import Word
from dictionary import get_fixed_length, get_synonyms


INFO = [
    "Colors:",
    "<div style='text-align: right; background-color: green; width: 20px; height: 20px; display: inline-block;'></div> Correct",
    "<div style='text-align: right; background-color: orange; width: 20px; height: 20px; display: inline-block;'></div> Present",
    "<div style='text-align: right; background-color: blue; width: 20px; height: 20px; display: inline-block;'></div> Svara Only",
    "<div style='text-align: right; background-color: purple; width: 20px; height: 20px; display: inline-block;'></div> Vyanjana Only",
    "<div style='text-align: right; background-color: red; width: 20px; height: 20px; display: inline-block;'></div> Svara and Vyanjana",
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
    print(st.session_state.synonyms)
    st.session_state.message = ""


true_word = st.session_state.true_word
word_length = len(true_word.aksharas)
max_attempts = 10

col_widths = [1 for _ in range(word_length)]
col_widths.append(2)
col_widths.append(3)

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

print(st.session_state.guesses)

render_grid()

if not st.session_state.game_over:
    guess = st.text_input("Enter your guess:")
    if st.button("Submit Guess"):
        guess_word = Word(guess)
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
            print(st.session_state.synonyms)
            st.session_state.message += ", ".join(st.session_state.synonyms["synonyms"])

        st.rerun()

if st.session_state.game_over:
    st.write(st.session_state.message)
    if st.button("Play Again"):
        st.session_state.current_row = 0
        st.session_state.guesses = [
            ["" for _ in range(word_length)] for _ in range(max_attempts)
        ]
        st.session_state.guess_status = [
            [CellStatus.ABSENT for _ in range(word_length)] for _ in range(max_attempts)
        ]
        st.session_state.game_over = False
        info = get_fixed_length(3)
        st.session_state.true_word = Word(info["word"])
        st.session_state.shloka = info["shloka"]
        st.session_state.synonyms = get_synonyms(info["word"])
        st.session_state.message = ""
        st.rerun()
