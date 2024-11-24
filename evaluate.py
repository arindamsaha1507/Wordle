"""Module to compare the word and guess Aksharas."""

from dataclasses import dataclass, field
from enum import Enum

from word_processor import Word


class CellStatus(Enum):
    """Enumeration to represent the status of a cell."""

    CORRECT = "correct"
    PRESENT = "present"
    SVARA_CORRECT = "svara_correct"
    VYANJANA_CORRECT = "vyanjana_correct"
    SVARA_AND_VYANJANA_CORRECT = "svara_and_vyanjana_correct"
    SVARA_ONLY = "svara_only"
    VYANJANA_ONLY = "vyanjana_only"
    SVARA_AND_VYANJANA = "svara_and_vyanjana"
    ABSENT = "absent"


@dataclass
class Compare:
    """Class to compare the word and guess Aksharas."""

    word: Word
    guess: Word

    status: list[CellStatus] = field(default_factory=list, init=False)

    def __post_init__(self):

        if isinstance(self.word, str):
            self.word = Word(self.word)
        if isinstance(self.guess, str):
            self.guess = Word(self.guess)

        if len(self.word.aksharas) != len(self.guess.aksharas):
            raise ValueError("Word and guess lengths do not match.")

        self.status = [CellStatus.ABSENT] * len(self.guess.aksharas)

    def compare(self):
        """Compare the word and guess Aksharas."""

        for index, akshara in enumerate(self.guess.aksharas):

            if self.word.is_akshara_correct(akshara, index):
                self.status[index] = CellStatus.CORRECT
            elif self.word.is_akshara_present(akshara):
                self.status[index] = CellStatus.PRESENT
            else:

                vyanjanas = self.guess.vyanjanas[index]
                svara = self.guess.svaras[index]

                vyanjana_check = any(
                    self.word.is_vyanjana_present(v) for v in vyanjanas
                )
                svara_check = self.word.is_svara_present(svara)

                svara_position_check = self.word.is_svara_correct(svara, index)
                vyanjana_position_check = any(
                    self.word.is_vyanjana_correct(v, index) for v in vyanjanas
                )

                if svara_position_check and vyanjana_position_check:
                    self.status[index] = CellStatus.SVARA_AND_VYANJANA_CORRECT

                elif svara_position_check:
                    self.status[index] = CellStatus.SVARA_CORRECT

                elif vyanjana_position_check:
                    self.status[index] = CellStatus.VYANJANA_CORRECT

                elif vyanjana_check and svara_check:
                    self.status[index] = CellStatus.SVARA_AND_VYANJANA
                elif vyanjana_check:
                    self.status[index] = CellStatus.VYANJANA_ONLY
                elif svara_check:
                    self.status[index] = CellStatus.SVARA_ONLY
                else:
                    self.status[index] = CellStatus.ABSENT
