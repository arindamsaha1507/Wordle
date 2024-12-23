"""Module to perform word processing tasks."""

from dataclasses import dataclass, field

from akshara import varnakaarya as vk

# import requests
# from requests.exceptions import HTTPError


SVARAS = ["अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ॠ", "ऌ", "ॡ", "ए", "ऐ", "ओ", "औ"]


@dataclass
class Word:
    """Class to interact with the Akshara API."""

    word: str
    aksharas: list[str] = field(default_factory=list, init=False)

    base_url: str = field(default="https://akshara-api.onrender.com", init=False)
    svaras: list[str] = field(default_factory=list, init=False)
    vyanjanas: list[list[str]] = field(default_factory=list, init=False)

    def __post_init__(self):
        """Fetch the Aksharas for the given word."""

        self.aksharas = self.fetch_aksharas(self.word)

        for akshara in self.aksharas:
            vinyaasa = self.fetch_vinyaasa(akshara)
            svara = [v for v in vinyaasa if v in SVARAS][0]
            vyanjana = [v for v in vinyaasa if v not in SVARAS]
            self.svaras.append(svara)
            self.vyanjanas.append(vyanjana)

    def fetch_vinyaasa(self, word: str) -> list[str]:
        """Fetch the Vinyaasas for a given word."""
        return vk.get_vinyaasa(word)

    def fetch_aksharas(self, word: str) -> list[str]:
        """Fetch the Aksharas for a given word."""
        return vk.get_akshara(word)

    def is_akshara_correct(self, akshara: str, index: int) -> bool:
        """Check if the given Akshara is correct at the given index."""
        return akshara == self.aksharas[index]

    def is_svara_correct(self, svara: str, index: int) -> bool:
        """Check if the given Svara is correct at the given index."""
        return svara == self.svaras[index]

    def is_vyanjana_correct(self, vyanjana: str, index: int) -> bool:
        """Check if the given Vyanjana is correct at the given index."""
        return vyanjana in self.vyanjanas[index]

    def is_akshara_present(self, akshara: str) -> bool:
        """Check if the given Akshara is present in the word."""
        return akshara in self.aksharas

    def is_svara_present(self, svara: str) -> bool:
        """Check if the given Svara is present in the word."""
        return svara in self.svaras

    def is_vyanjana_present(self, vyanjana: str) -> bool:
        """Check if the given Vyanjana is present in the word."""
        vyanjana_flat = [v for v_list in self.vyanjanas for v in v_list]
        return vyanjana in vyanjana_flat

    def get_svara_signature(self) -> list[str]:
        """Return the Svara signature of the word."""

        signature = []

        for akshara in self.aksharas:
            vinyaasa = self.fetch_vinyaasa(akshara)
            svara = [v for v in vinyaasa if v in SVARAS][0]
            signature.append(svara)

        return signature

    def get_vyanjana_signature(self) -> list[list[str]]:
        """Return the Vyanjana signature of the word."""

        signature = []

        for akshara in self.aksharas:
            vinyaasa = self.fetch_vinyaasa(akshara)
            vyanjana = [v if v not in SVARAS else "-" for v in vinyaasa]
            signature.append(vyanjana)

        return signature
