import pytest
import genanki
from src.word import Word

def test_has_attr_word():
    """
    Test that the Word class has the 'word' attribute.
    """
    # Create Word objects with valid inputs
    word1 = Word("给", "mandarin")
    word2 = Word("Espejo", "spanish")

    # Check if the 'word' attribute exists in both objects
    assert hasattr(word1, "word")
    assert hasattr(word2, "word")

def test_invalid_input_word():
    """
    Test that the Word class raises ValueError for invalid inputs.
    """
    # Test that a ValueError is raised for an empty string
    with pytest.raises(ValueError, match="Word must be a non-empty string"):
        Word("", "Spanish")  # Empty string

    # Test that a ValueError is raised for non-string inputs
    with pytest.raises(ValueError, match="Word must be a non-empty string"):
        Word(12345, "Themne")  # Integer input

    # Test that a ValueError is raised for None input
    with pytest.raises(ValueError, match="Word must be a non-empty string"):
        Word(None, "Mende")  # None input

    # Test that a ValueError is raised for emojis and punctuation
    with pytest.raises(ValueError, match="Word must contain normal characters"):
        Word("😀", "krio")  # Emoji input

    with pytest.raises(ValueError, match="Word must contain normal characters"):
        Word("!", "mandarin")  # Punctuation input

    with pytest.raises(ValueError, match="Word must contain normal characters"):
        Word("?", "chinese")  # Punctuation input

def test_has_attr_known_word():
    """
    Test that the Word class has the 'known_word' attribute.
    """
    # Create a Word object
    word1 = Word("どこ", "japanese")

    # Check if the 'known_word' attribute exists
    assert hasattr(word1, "known_word")

def test_is_known_word():
    """
    Test the behavior of the 'known_word' attribute for various inputs.
    """
    # Test with a word that is not known
    word1 = Word("どこ", "japanese")
    assert word1.known_word == False

    # Test with a word that is known
    word2 = Word("火车", "chinese")
    assert word2.known_word == True

    # Test with a single character that is not known
    word_single_char = Word("A", "english")
    assert word_single_char.known_word == False

    # Test with a word that is not known
    word3 = Word("辦", "mandarin")
    assert word3.known_word == False

    # Test with whitespace characters
    word4 = Word(" ", "english")
    word_ws = Word(" 辦法 ", "mandarin")
    word_tab = Word("\t", "japanese")
    word_newline = Word("\n", "mandarin")
    word_multiple_spaces = Word("   ", "mandarin")

    assert word_tab.known_word == False
    assert word_newline.known_word == False
    assert word_multiple_spaces.known_word == False
    assert word_ws.known_word == True
    assert word4.known_word == False

    # Test with a very long word
    word_long = Word("a" * 1000, "mandarin")
    assert word_long.known_word == False

    # Test with a numeric word
    word_number = Word("123", "mandarin")
    assert word_number.known_word == False

    # Test with a mixed word (letters and known word)
    word_mixed = Word("A火车", "mandarin")
    assert word_mixed.known_word == False

def test_language():
    word1 = Word("和", "Mandarin")
    word2 = Word("Espejo", "Spanish")
    word3 = Word("どこ", "Japanese")

    assert word1.lang == "mandarin"
    assert word2.lang == "spanish"
    assert word3.lang == "japanese"

    # Test that a ValueError is raised for non-string inputs
    with pytest.raises(ValueError, match="Language must be a non-empty string"):
        Word("和", 12345)  # Integer input

    # Test that a ValueError is raised for None input
    with pytest.raises(ValueError, match="Language must be a non-empty string"):
        Word("和", None)  # None input

    # Test that a ValueError is raised for emojis and punctuation
    with pytest.raises(ValueError, match="Language must contain normal characters"):
        Word("Espejo", "😀")  # Emoji input

def test_definition():
    # Test that definition is intialized correctly with normal input
    word1 = Word("和", "Mandarin", "and")

    assert word1.definition == "and"

    # Test that definition is intialized correcly with blank input
    word2 = Word("和", "Mandarin")
    
    assert word2.definition == ""

class TestToStr():
    """
    This class is meant to test the functionality of the
    __str__ function
    """

    def test_word_to_string_val_in(self):
        word = Word("釣り用語".strip().lower(),"Japanese")

        assert word.__str__() == f"Word({'釣り用語'.strip().lower()},japanese,,./data/known.csv,False)"

    def test_word_with_definition_to_string(self):
        """Test __str__ functionality with a definition provided"""
        word = Word("test", "English", definition="a procedure intended to establish quality")
        assert word.__str__() == f"Word(test,english,a procedure intended to establish quality,./data/known.csv,False)"

    def test_word_with_known_status_to_string(self):
        """Test __str__ functionality with known status set to True"""
        word = Word("找", "English")
        assert word.__str__() == f"Word(找,english,,./data/known.csv,True)"

class TestWordGetVocabNote:
    """
    tests if the get_vocab_note() function works properly
    """

    def test_get_vocab_note_with_val_input(self):
        """
        test whether function returns expected fields given correct
        in
        """
        word = Word("雷霆", "Chinese")

        assert hasattr(word, "vocab_note")
        assert word.vocab_note is not None

class TestWordGetVocabFields:
    def test_get_vocab_fields_with_val_input(self):
        """
        test whether function get fields returns valid input
        when given correct in
        """
        word = Word("雷霆", "Chinese")
        
        vocab_fields = word.get_vocab_fields()

        assert isinstance(vocab_fields, dict)

        assert "雷霆" in vocab_fields["word"]

class TestWordGeVocabtModel:
    """
    Tests the function that creates a genanki note model that
    is passed to genanki.Note()
    """
    
    def test_word_get_vocab_model_val_in(self):
        """
        tests get model to ensure that it works with correct in
        """
        word = Word("雷霆", "Chinese")

        vocab_model = word.get_vocab_model()

        assert isinstance(vocab_model, genanki.Model)
        assert False

