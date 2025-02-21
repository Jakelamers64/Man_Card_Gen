import pytest

from src.word import Word

def test_has_attr_word():
    #create word object
    word1 = Word("给")
    word2 = Word("Espejo")

    #check if word has word attribute
    assert hasattr(word1,"word")
    assert hasattr(word2,"word")

def test_invalid_input_word():
    #check if error was thrown for invalid input blank
    with pytest.raises(ValueError, match="Name must be a non-empty string"):
        Word("")  # Empty name

    # Test that a ValueError is raised when the word is not a string
    with pytest.raises(ValueError, match="Name must be a non-empty string"):
        Word(12345)  # Invalid type for name (should be a string)

