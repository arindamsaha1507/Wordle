"""Module to compare the word and guess Aksharas."""

from dataclasses import dataclass, field
from enum import Enum

from word_processor import Word


class CellStatus(Enum):
    """Enumeration to represent the status of a cell."""

    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"

    MISSING = "missing"
    MISMATCH = "mismatch"


@dataclass
class Compare:
    """Class to compare the word and guess Aksharas."""

    word: Word
    guess: Word

    status: list[tuple[CellStatus, CellStatus]] = field(
        default_factory=list, init=False
    )

    def __post_init__(self):

        if isinstance(self.word, str):
            self.word = Word(self.word)
        if isinstance(self.guess, str):
            self.guess = Word(self.guess)

        if len(self.word.aksharas) != len(self.guess.aksharas):
            raise ValueError("Word and guess lengths do not match.")

        self.status = [(CellStatus.ABSENT, CellStatus.ABSENT)] * len(
            self.guess.aksharas
        )

    def compare(self):
        """Compare the word and guess Aksharas."""

        word_svara_signature = self.word.get_svara_signature()
        word_vyanjana_signature = self.word.get_vyanjana_signature()

        word_vyanjana_signature_flat = [
            v for v_list in word_vyanjana_signature for v in v_list
        ]

        guess_svara_signature = self.guess.get_svara_signature()
        guess_vyanjana_signature = self.guess.get_vyanjana_signature()

        if len(word_svara_signature) != len(guess_svara_signature):
            raise ValueError("Word and guess svara signatures do not match.")

        length = len(word_svara_signature)

        for ii in range(length):

            word_svara_sig = word_svara_signature[ii]
            word_vyanjana_sig = word_vyanjana_signature[ii]

            guess_svara_sig = guess_svara_signature[ii]
            guess_vyanjana_sig = guess_vyanjana_signature[ii]

            if word_svara_sig == guess_svara_sig:
                svara_status = CellStatus.CORRECT
            elif guess_svara_sig in word_svara_signature:
                svara_status = CellStatus.PRESENT
            else:
                svara_status = CellStatus.ABSENT

            if word_vyanjana_sig == guess_vyanjana_sig:
                vyanjana_status = CellStatus.CORRECT
            else:

                vyanjana_status = CellStatus.ABSENT

                for vyanjana in guess_vyanjana_sig:

                    if vyanjana == "-":
                        continue

                    if vyanjana in word_vyanjana_signature[ii]:
                        vyanjana_status = CellStatus.MISSING
                        break

                    if vyanjana in word_vyanjana_signature_flat:
                        vyanjana_status = CellStatus.PRESENT

            self.status[ii] = (vyanjana_status, svara_status)
