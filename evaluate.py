"""Module to compare the word and guess Aksharas."""

from dataclasses import dataclass, field
from enum import Enum

from word_processor import Word, SVARAS


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

        self.degrade()

    def degrade(self):
        """Degrade the status to MISSING if required."""

        word_svaras = self.word.svaras
        word_vyanjanas = [v for v_list in self.word.vyanjanas for v in v_list]
        word_varnas = word_svaras + word_vyanjanas
        word_varna_count = {varna: word_varnas.count(varna) for varna in word_varnas}

        current_status_dict = {}

        for index, akshara in enumerate(self.guess.aksharas):

            vinyaasa = self.guess.fetch_vinyaasa(akshara)

            for v in vinyaasa:

                if v in SVARAS:
                    status = self.status[index][1]
                else:
                    status = self.status[index][0]

                if v in current_status_dict:
                    current_status_dict[v].append(status)
                else:
                    current_status_dict[v] = [status]

        for key in current_status_dict:
            current_status_dict[key] = (
                current_status_dict[key].count(CellStatus.CORRECT)
                + current_status_dict[key].count(CellStatus.MISSING)
                + current_status_dict[key].count(CellStatus.PRESENT)
            )

        for key, value in current_status_dict.items():

            if key in word_varna_count and value > word_varna_count[key]:

                diff = value - word_varna_count[key]

                index = 1 if key in SVARAS else 0

                while diff > 0:

                    diff = self.reduce(key, index, diff)

    def reduce(self, key, index, diff):
        """Reduce the status to MISSING if required."""

        for ii, _ in enumerate(self.guess.aksharas):

            if self.status[ii][index] == CellStatus.PRESENT and (
                key in self.guess.vyanjanas[ii] or key == self.guess.svaras[ii]
            ):

                self.status[ii] = (
                    (CellStatus.ABSENT if index == 0 else self.status[ii][0]),
                    (CellStatus.ABSENT if index == 1 else self.status[ii][1]),
                )
                diff -= 1

                if diff == 0:
                    break

        return diff
