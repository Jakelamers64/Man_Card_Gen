import pytest

from src.sentence import Sentence

def test_init_with_valid_inputs():
    sentence_man = Sentence("我星期四要去香港")

    assert hasattr(sentence_man, "sentence")
