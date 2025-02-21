class Word:
    def __init__(self, word):
        if not isinstance(word, str) or not word:
            raise ValueError("Name must be a non-empty string")

        self.word = word
