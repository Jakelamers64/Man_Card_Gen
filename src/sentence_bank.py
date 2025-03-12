import pandas as pd
import re

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
        self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]] = pd.to_numeric(self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]].astype(float))
        # Validate that all ratios are between 0 and 1
        if not self.sentence_bank[REQUIRED_SENTENCE_BANK_COLUMNS[2]].between(0, 1, inclusive="both").all():
            raise ValueError("Custom Ratios must be between 0 and 1")

    def get_sentences(self, word, num_sentences):
        """
        Get sentences containing the specified word.
        
        Parameters:
        word (str): Word to search for in sentences
        num_sentences (int): Number of sentences to return
        
        Returns:
        list: List of dictionaries containing matching sentences
        
        Raises:
        ValueError: If inputs are invalid
        """
        # Validate inputs
        if not isinstance(word, str) or not word:
            raise ValueError("Word must be non-empty string")
            
        if not isinstance(num_sentences, int) or num_sentences <= 0:
            raise ValueError("Num_sentences must be a int greater than zero and less than len(sentences.tsv)")
            
        if num_sentences > len(self.sentence_bank):
            raise ValueError("Num_sentences must be a int greater than zero and less than len(sentences.tsv)")
            
        # Create a safe pattern for case-insensitive search
        # This handles special regex chars by escaping them
        search_pattern = re.escape(word)
        
        # Find matching sentences (case insensitive)
        matches = self.sentence_bank[self.sentence_bank["Sentence"].str.contains(search_pattern, case=False, regex=True, na=False)]
        
        # Sort by Custom Ratio (descending)
        sorted_matches = matches.sort_values(by="Custom Ratio", ascending=False)
        
        # Limit to requested number of sentences (or all if fewer matches exist)
        limit = min(num_sentences, len(sorted_matches))
        top_matches = sorted_matches.head(limit)
        
        # Convert to list of dictionaries
        result = []
        for _, row in top_matches.iterrows():
            result.append({
                "Sentence": row["Sentence"],
                "Meaning": row["Meaning"],
                "Custom Ratio": row["Custom Ratio"]
            })
            
        return result

    def rank_sentences(self, known_words_path):
        """
        Rank sentences based on the ratio of known words they contain.
        
        Parameters:
        -----------
        known_words_path : str
            Path to the CSV file containing known words
        """
        # If the sentence bank is empty, return early
        if len(self.sentence_bank) == 0:
            return
            
        # Load known words
        try:
            known_df = pd.read_csv(known_words_path)
            # Convert to lowercase for case-insensitive matching and handle empty dataframe
            if 'known' in known_df.columns and not known_df.empty:
                known_words = set(word.lower() for word in known_df['known'] if isinstance(word, str))
            else:
                known_words = set()
        except (pd.errors.EmptyDataError, FileNotFoundError):
            known_words = set()
            
        # Process each sentence to calculate the ratio of known words
        for idx, row in self.sentence_bank.iterrows():
            if not isinstance(row['Sentence'], str) or not row['Sentence'].strip():
                self.sentence_bank.at[idx, 'Custom Ratio'] = 0
                continue
                
            # Get words from the sentence, handling various scripts and punctuation
            sentence = row['Sentence']
            
            # For languages using spaces (like English, Spanish, etc.)
            if any(ord(c) < 128 for c in sentence):  # Contains ASCII chars
                # Remove punctuation and split by whitespace
                words = re.sub(r'[^\w\s]', ' ', sentence.lower()).split()
            else:
                # For languages like Chinese where characters are words
                words = list(sentence.lower())
                # Remove punctuation characters
                words = [w for w in words if not re.match(r'[^\w]', w, re.UNICODE)]
            
            # Skip empty sentences
            if not words:
                self.sentence_bank.at[idx, 'Custom Ratio'] = 0
                continue
                
            # Count known words
            known_count = sum(1 for word in words if word.lower() in known_words)
            
            # Calculate and store the ratio
            if words:
                ratio = known_count / len(words)
                self.sentence_bank.at[idx, 'Custom Ratio'] = ratio
            else:
                self.sentence_bank.at[idx, 'Custom Ratio'] = 0
    
    def add_sentence():
        pass
