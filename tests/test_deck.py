import pytest

from src.deck import Deck

def test_one():
    assert 0 == 1

def test_two():
    assert 0 == 0


class testDeckInit:
    """
    A class for testing different inputs to the deck class
    
    Should take a non-empty list of strings
    """

    def test_deck_init_valid_input():
        """
        tests to see if word attr is created when valid input is used
        """
        simple_deck = Deck(["test","test","test"])

        assert hasattr(simple_deck, "words")

    def test_deck_init_with_non_list():
        with pytest.raises(ValueError):
            Deck("Needs a list")
