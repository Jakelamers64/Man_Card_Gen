import pandas as pd
import regex
import genanki

class Word:
    def __init__(self, word, language, definition="",  path_to_known_csv="./data/known.csv"):
        """
        Initialize a Word object.

        Args:
            word (str): The word to be processed. Must be a non-empty string containing valid characters.
            language (str): The language of the word. Must be a non-empty string containing valid characters.
            definition (str): The words defintion in you native language defaults to ""
            path_to_known_csv (str): Path to the CSV file containing known words. Defaults to "./data/known.csv".

        Raises:
            ValueError: If the word is not a non-empty string or contains invalid characters.
            ValueError: If the language is not a non-empty string or cotains invalid characters.
        """
        # Validate input word
        if not isinstance(word, str) or not word:
            raise ValueError("Word must be a non-empty string")

        if not self.is_valid_string(word):
            raise ValueError("Word must contain normal characters")

        # Normalize the word by stripping whitespace and converting to lowercase
        self.word = word.strip().lower()

        # Validate lang input
        if not isinstance(language, str) or not language:
            raise ValueError("Language must be a non-empty string")

        if not self.is_valid_string(language):
            raise ValueError("Language must contain normal characters")

        # Normalize the lang and save it
        self.lang = language.strip().lower()

        # Validate definition input
        if not isinstance(definition, str):
            raise ValueError("Definition must be a string")

        # Normalize the definition and save it
        self.definition = definition

        # Store the path to the known words CSV file
        self.path_to_known_csv = path_to_known_csv

        # Determine if the word is known
        self.known_word = self.is_known_word()

        # Hardcoded Model ID
        self.vocab_model_id = 275837465987236587

        if not self.known_word:
            self.vocab_note = self.get_vocab_note()
        else:
            self.vocab_note = None

    def get_vocab_note(self):
        return genanki.Note(
                    model = self.get_vocab_model(),
                    fields = self.get_vocab_fields()
                )

    def get_vocab_fields(self):
        """
        returns a dict containing the following fields for
        genanki.Note constructor field arg
        """
        return {
                    "word": self.word
                }



    def get_vocab_model(self):
        return genanki.Model(
                    model_id = self.vocab_model_id,
                    name = 'Vocab Card',
                    fields = [{'name':key} for key in self.get_vocab_fields().keys()]
                )

    def is_known_word(self):
        """
        Check if the word is in the list of known words.

        Returns:
            bool: True if the word is known, False otherwise.
        """
        # Load the known words from the CSV file
        known_df = pd.read_csv(self.path_to_known_csv)

        # Check if the word matches any entry in the first column of the CSV
        return any(self.word == i.strip() for i in known_df[known_df.columns[0]])

    def is_valid_string(self, s):
        """
        Validate if the string contains only valid characters (letters, numbers, and whitespace).

        Args:
            s (str): The string to validate.

        Returns:
            bool: True if the string is valid, False otherwise.
        """
        # Regex pattern:
        # \p{L}: Matches any kind of letter from any language.
        # \p{N}: Matches any kind of numeric character.
        # \s: Matches whitespace.
        pattern = r'^[\p{L}\p{N}\s]+$'

        # Use the regex to test the string
        return bool(regex.match(pattern, s))

    def __str__(self):
        return f"Word({self.word},{self.lang},{self.definition},{self.path_to_known_csv},{self.known_word})"
