import pandas as pd

class Sentence_bank:
    def __init__(self, path_to_sentences_tsv=r"./data/sentences.tsv"):

        if not isinstance(path_to_sentences_tsv,str) or path_to_sentences_tsv is None:
            raise ValueError("path_to_sentences_tsv must be a non-empty string")
        
        if not path_to_sentences_tsv.split(r'.')[-1] == "tsv":
            raise ValueError("path_to_sentences_tsv must end with .tsv")

        self.sentence_bank = pd.read_csv(path_to_sentences_tsv,sep='\t')
