import pandas as pd

class Sentence_bank:
    """
    A class for loading and validating a bank of sentences from a TSV file.
    
    The TSV file must contain at least three columns:
    - "Sentence": The text of the sentence
    - "Meaning": The meaning or interpretation of the sentence
    - "Custom Ratio": A numeric value between 0 and 1
    """
    
    def __init__(self, path_to_sentences_tsv="./data/sentences.tsv"):
        """
        Initialize the SentenceBank by loading and validating the sentences TSV file.
        
        Args:
            path_to_sentences_tsv (str): Path to the TSV file containing sentences.
                                         Defaults to "./data/sentences.tsv".
                                         
        Raises:
            ValueError: If the path is invalid, file format is incorrect,
                        required columns are missing, duplicate sentences exist,
                        or custom ratios are out of range.
        """
        # Validate the path parameter
        if not isinstance(path_to_sentences_tsv, str) or path_to_sentences_tsv is None:
            raise ValueError("path_to_sentences_tsv must be a non-empty string")
        
        if not path_to_sentences_tsv.split('.')[-1] == "tsv":
            raise ValueError("path_to_sentences_tsv must end with .tsv")
        
        # Load the TSV file into a pandas DataFrame
        self.sentence_bank = pd.read_csv(
            path_to_sentences_tsv,
            sep='\t'
        )
        
        # Define required columns and validate their presence
        REQUIRED_SENTENCE_BANK_COLUMNS = ["Sentence", "Meaning", "Custom Ratio"]
        for column_name in REQUIRED_SENTENCE_BANK_COLUMNS:
            if column_name not in self.sentence_bank.columns:
                raise ValueError(
                    f"Column {column_name} not found. Expected at least '{REQUIRED_SENTENCE_BANK_COLUMNS}', "
                    f"but found {self.sentence_bank.columns}"
                )
        
        # Process and validate the Sentence column
        # Fill any NaN values with empty strings
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]] = self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]].fillna("")
        # Strip whitespace from each sentence
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]] = [
            i.strip() for i in self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]]
        ]
        
        # Check for duplicate sentences
        if self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]].duplicated().any():
            for idx, row in self.sentence_bank.loc[
                self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[0]].duplicated(), :
            ].iterrows():
                print(row)
                # Commented out code to remove duplicated rows
                # self.sentence_bank = self.sentence_bank.drop(idx)
            # self.sentence_bank.to_csv(path_to_sentences_tsv, sep="\t")
            raise ValueError("Sentence column cannot contain duplicates")
        
        # Process and validate the Meaning column
        # Fill any NaN values with empty strings
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[1]] = self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[1]].fillna("")
        # Strip whitespace from each meaning
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[1]] = [
            i.strip() for i in self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[1]]
        ]
        
        # Process and validate the Custom Ratio column
        # Fill any NaN values with 0
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]] = self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]].fillna(0)
        # Convert to numeric values
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]] = pd.to_numeric(self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]])
        # Validate that all ratios are between 0 and 1
        if not self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]].between(0, 1, inclusive="both").all():
            raise ValueError("Custom Ratios must be between 0 and 1")
