"""This module contains the functions to render the grid of Aksharas."""

import streamlit as st
from evaluate import CellStatus


cell_colors_dict = {
    CellStatus.CORRECT: "green",
    CellStatus.PRESENT: "orange",
    CellStatus.ABSENT: "gray",
    CellStatus.MISSING: "darkblue",
    CellStatus.MISMATCH: "red",
}


def grid_cell_markdown(akshara: str, status: CellStatus) -> str:
    """Return the HTML for a grid cell."""

    cell_color_1 = cell_colors_dict[status[0]]
    cell_color_2 = cell_colors_dict[status[1]]
    return f"<div style='text-align: center; background: linear-gradient(90deg, {cell_color_1} 50%, {cell_color_2} 50%); color: white; height: 50px; line-height: 50px; margin-bottom: 10px;'>{akshara}</div>"


# Render the Grid
def render_grid(word_length: int, max_attempts: int, helper_text: list):
    """Render the grid of Aksharas."""

    col_widths = [2 / word_length for _ in range(word_length)]
    col_widths.append(0.1)
    col_widths.append(4)

    col_widths = [width / sum(col_widths) for width in col_widths]

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
                if row < len(helper_text):
                    col.markdown(helper_text[row], unsafe_allow_html=True)
