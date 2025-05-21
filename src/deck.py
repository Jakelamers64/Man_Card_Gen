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
        pass
