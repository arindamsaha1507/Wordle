"""Backend App for the Word Guessing Game"""

import pathlib
import time
import streamlit as st

from akshara import varnakaarya as vk
from dictionary import is_word_in_dictionary


files = pathlib.Path("data").rglob("*.csv")
files = list(files)

if "current_file" not in st.session_state:
    st.session_state.current_file_index = 0
    st.session_state.current_file = files[0]
    st.session_state.file_selected = False
    st.session_state.new_words = set()

filenames = [file.as_posix() for file in files]


if not st.session_state.file_selected:

    current_file = st.selectbox(
        "Select a file", options=filenames, index=st.session_state.current_file_index
    )

    if st.button("Select"):
        st.session_state.current_file = current_file
        st.session_state.current_file_index = filenames.index(current_file)
        st.session_state.file_selected = True
        st.rerun()


if st.session_state.file_selected:
    current_file = st.session_state.current_file

    with open(current_file, "r", encoding="utf-8") as file:
        words = file.readlines()[0]

    words = words.split(",")
    words = set(words)

    words = words.union(st.session_state.new_words)

    aksharas = [len(vk.get_akshara(word)) for word in words]
    letterwise_counts = {i: aksharas.count(i) for i in set(aksharas)}

    st.write(f"## Editing {current_file}")

    st.write("### Summary")
    st.write(f"Current number of words: {len(words)}")
    for key, value in letterwise_counts.items():
        st.write(f"Number of words with {key} aksharas: {value}")

    st.write("### Add a word")
    new_word = st.text_input("Enter the new word")
    if st.button("Add"):

        if not is_word_in_dictionary(new_word):
            st.error("Word not found in the dictionary")
            time.sleep(5)

        elif new_word in words:
            st.error("Word already present in the file")
            time.sleep(5)
        else:
            words.add(new_word)
            st.session_state.new_words.add(new_word)

        st.rerun()

    st.write("### Words added so far")
    for word in st.session_state.new_words:
        st.write(word)

    st.write("### Remove a word")
    word_to_remove = st.text_input("Enter the word to remove")
    if st.button("Remove"):
        words.remove(word_to_remove)
        if word_to_remove in st.session_state.new_words:
            st.session_state.new_words.remove(word_to_remove)

        st.rerun()

    st.write("### Save the changes")
    if st.button("Save"):
        with open(current_file, "w", encoding="utf-8") as file:
            file.write(",".join(words))

        st.write("Changes saved successfully")
        st.session_state.new_words = set()
        st.session_state.file_selected = False
        time.sleep(5)
        st.rerun()
