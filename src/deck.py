import genanki

from random import randint
from src.word import Word

class Deck:
    #@FIXME Figure out how to handle language
    def __init__(self, input_words: list, language="en"):
        if not isinstance(input_words,list):
            raise ValueError

        if input_words is None or len(input_words) < 1:
            raise ValueError

        if any([not isinstance(elem,str) for elem in input_words]):
            raise TypeError

        if any([len(elem) < 1 for elem in input_words]):
            raise ValueError

        self.input_words = input_words

        self.words = []

        for word in self.input_words:
            self.words.append(Word(word,language))

    def create_deck(self):
        self.deck = genanki.Deck(
                    randint(10**(15-1),(10*15)-1),
                    "To Add"
                )

        self.media = list()

        for word in self.input_words:
            self.deck.add_note(word.get_note())
            self.media.extend(word.get_media())

        self.package = genanki.Package(self.deck)
        self.package.media_files = self.media
