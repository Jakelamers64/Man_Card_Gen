import pytest

from src.deck import Deck
from src.word import Word

class TestDeckInit:
    """
    A class for testing different inputs to the deck class
    
    Should take a non-empty list of strings
    """

    def test_deck_init_valid_list_of_strings(self):
        """
        tests to see if word attr is created when valid input is used
        """
        simple_deck = Deck(["test","test","test"])

        assert hasattr(simple_deck, 'input_words')

    def test_deck_init_with_empty_list(self):
        """
        Tests that the Deck raises ValueError when initialized 
        with an empty list
        """
        with pytest.raises(ValueError):
            Deck([])

    def test_deck_init_with_non_list(self):
        """
        Tests that the Deck raises a ValueError when initialized with
        a string
        """
        with pytest.raises(ValueError):
            Deck("Needs a list")

    def test_deck_init_with_non_string_elements(self):
        """
        Tests that the Deck raises TypeError when list contains non-string 
        elements
        """
        with pytest.raises(TypeError):
            Deck(["word1", 123, "word2"])
    
    def test_deck_init_with_none_value(self):
        """
        Tests that the Deck raises ValueError when initialized with None
        """
        with pytest.raises(ValueError):
            Deck(None)

    def test_deck_init_with_empty_strings(self):
        """
        Tests that the Deck handles empty strings in the list
        """
        with pytest.raises(ValueError):
            Deck(["word1", "", "word2"])

    def test_deck_init_with_nested_lists(self):
        """
        Tests that the Deck raises TypeError when initialized with nested lists
        """
        with pytest.raises(TypeError):
            Deck(["word1", ["nested", "list"], "word2"])

class TestDeckWords:
    """
    Class deck will have a list of word objects
    """
    
    def test_deck_words_creation_with_val(self):
        simple_deck = Deck(["Hola","蝶々","魚桿"])

        assert hasattr(simple_deck, "words")
    

    def test_deck_words_elem_types(self):
        simple_deck = Deck(["Hola","魚桿","釣り用語"])

        for elem in simple_deck.words:
            assert isinstance(elem, Word)
