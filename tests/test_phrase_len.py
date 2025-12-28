import pytest

class TestPhraseLen:
    def test_phrase_len_grant(self):
        phrase = input("Set a phrase <15 symbols: ")
        assert len(phrase) < 15, f"The phrase is too long ({len(phrase)} >=15 symbols): {phrase}"