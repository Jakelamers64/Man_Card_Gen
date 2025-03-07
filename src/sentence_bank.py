import pandas as pd

class Sentence_bank:
    def __init__(self, path_to_sentences_tsv=r"./data/sentences.tsv"):

        if not isinstance(path_to_sentences_tsv,str) or path_to_sentences_tsv is None:
            raise ValueError("path_to_sentences_tsv must be a non-empty string")
        
        if not path_to_sentences_tsv.split(r'.')[-1] == "tsv":
            raise ValueError("path_to_sentences_tsv must end with .tsv")

        self.sentence_bank = pd.read_csv(
                path_to_sentences_tsv,
                sep='\t'
                )

        REQUIRED_SENTENCE_BANK_COLUMNS = ["Sentence","Meaning","Custom Ratio"]

        for column_name in REQUIRED_SENTENCE_BANK_COLUMNS:
            if column_name not in self.sentence_bank.columns:
                raise ValueError(f"Column {column_name} not found. Expected at least '{REQUIRED_SENTENCE_BANK_COLUMNS}', but found {self.sentence_bank.columns}")

        # Processing Sentence column
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]] =  self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]].fillna("")
        
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]] = [ i.strip() for i in self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]]]

        if self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]].duplicated().any():

            for idx, row in self.sentence_bank.loc[self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]].duplicated(),:].iterrows():
                print(row)

                # Code to remove duplicated rows
                #self.sentence_bank = self.sentence_bank.drop(idx)

            #self.sentence_bank.to_csv(path_to_sentences_tsv,sep="\t")

            raise ValueError("Sentence column can not contain duplicates")

        # Processing Meaning Column
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[1]] =  self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[1]].fillna("")

        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[1]] = [ i.strip() for i in self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[1]]]

        # Processing Custom Ratio
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]] =  self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]].fillna(0)
        
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]] = pd.to_numeric(self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]])

        if not self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]].between(0,1,inclusive="both").all():
            raise ValueError("Custom Ratios must be between 0 and 1")
