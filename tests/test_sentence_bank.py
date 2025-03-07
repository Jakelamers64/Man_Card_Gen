import tempfile
import os
import pytest
import pandas as pd

from src.sentence_bank import Sentence_bank

def test_has_sentence_bank_attr():
    """
    Test the Sentence_bank class to ensure it properly initializes with a sentence_bank attribute
    and handles various error conditions appropriately.
    """
    
    # Test initialization with default constructor
    sentence_bank1 = Sentence_bank() 
    # Test initialization with valid file path
    sentence_bank2 = Sentence_bank("./data/sentences.tsv")
                                        
    # Verify both instances have the sentence_bank attribute
    assert hasattr(sentence_bank1, "sentence_bank")
    assert hasattr(sentence_bank2, "sentence_bank")
                                                        
    # Verify the type of sentence_bank attribute (adjust as needed for implementation)
    assert isinstance(sentence_bank1.sentence_bank, pd.DataFrame)
    assert isinstance(sentence_bank2.sentence_bank, pd.DataFrame)
                                                                        
    # Test error handling for non-existent file
    incorrect_file_path = "./data/chinese_sentences.tsv"   
    
    with pytest.raises(FileNotFoundError):
        sentence_bank3 = Sentence_bank(incorrect_file_path)
                                                                                                    
    # Test error handling for empty string path
    incorrect_file_path = ""

    with pytest.raises(ValueError): 
        sentence_bank4 = Sentence_bank(incorrect_file_path)

    # Test error handling for directory path instead of file
    directory_path = "./data/"

    with pytest.raises(ValueError):
        sentence_bank6 = Sentence_bank(directory_path)

    # Test error handling for None path
    with pytest.raises(ValueError):
        sentence_bank9 = Sentence_bank(None)

    # Test error handling for incorrect path type (integer)
    with pytest.raises(ValueError):
        sentence_bank10 = Sentence_bank(123)

    # Create temporary directory for file-based tests
    with tempfile.TemporaryDirectory() as tempdir:
        # Test invalid file format
        tmpfilepath = os.path.join(tempdir, 'invalid_format.txt')

        with open(tmpfilepath, "w") as file:
            file.write("test")

        with pytest.raises(ValueError):
            sentence_bank5 = Sentence_bank(tmpfilepath)

        # Test file with no read permissions
        tmpfilepath = os.path.join(tempdir, 'no_permission.tsv')

        # Create a basic valid sentence bank DataFrame
        no_permission = pd.DataFrame({
            "Sentence": ["Hola! Como estas?"],
            "Meaning": ["Hello! How are you?"],
            "Custom Ratio": [1.0]
            })

        no_permission.to_csv(tmpfilepath, sep="\t")

        # Remove all permissions from the file
        os.chmod(tmpfilepath, 0o000)

        with pytest.raises(PermissionError):
            sentence_bank7 = Sentence_bank(tmpfilepath)

        # Test empty file handling
        tmpfilepath = os.path.join(tempdir, 'empty.tsv')

        # Create an empty DataFrame
        empty = pd.DataFrame({
            "Sentence": [],
            "Meaning": [],
            "Custom Ratio": []
            })

        empty.to_csv(tmpfilepath, sep="\t")

        sentence_bank8 = Sentence_bank(tmpfilepath)

        # Verify that empty file creates an empty sentence bank
        assert len(sentence_bank8.sentence_bank) == 0

def test_sentence_bank_creation():
    """
    Test function for the Sentence_bank class initialization.
    This function tests various scenarios for creating a Sentence_bank object,
    including handling of different file formats, missing columns, and edge cases.
    """
    # Define required columns that should be present in a valid Sentence_bank
    columns = [
        "Sentence",
        "Meaning",
        "Custom Ratio"
    ]
    
    # Use a temporary directory for all test files
    with tempfile.TemporaryDirectory() as tempdir:
        #----------------------------------------------------------------------
        # Test Case 1: Basic valid sentence bank
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'normal.tsv')
        
        # Create a simple, valid sentence bank
        normal = pd.DataFrame({
            "Sentence": ["Hola! Como estas?"],
            "Meaning": ["Hello! How are you?"],
            "Custom Ratio": [1.0]
        })
        normal.to_csv(tmpfilepath, sep="\t")
        
        # Initialize Sentence_bank with the file and verify required columns exist
        sentence_bank5 = Sentence_bank(tmpfilepath)
        for column in columns:
            assert column in sentence_bank5.sentence_bank.columns
            
        #----------------------------------------------------------------------
        # Test Case 2: Sentence bank with extra columns (should work)
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'more_than_nec.tsv')
        
        # Create a sentence bank with additional columns beyond requirements
        more_than_nec = pd.DataFrame({
            "Sentence": ["很好，谢谢。"],
            "Pinyin": ["hěn hǎo xièxie"],
            "Meaning": ["Fine, thanks."],
            "HSK average": [1],
            "Custom Ratio": [1]
        })
        more_than_nec.to_csv(tmpfilepath, sep="\t")
        
        # Initialize and verify the required columns exist
        sentence_bank6 = Sentence_bank(tmpfilepath)
        for column in columns:
            assert column in sentence_bank6.sentence_bank.columns
            
        #----------------------------------------------------------------------
        # Test Case 3: Missing required column (should fail)
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'no_meaning.tsv')
        
        # Create a sentence bank missing the "Meaning" column
        no_meaning = pd.DataFrame({
            "Sentence": ["很好，谢谢。"],
            "Pinyin": ["hěn hǎo xièxie"],
            "HSK average": [1],
            "Custom Ratio": [1]
        })
        no_meaning.to_csv(tmpfilepath, sep="\t")
        
        # Verify that ValueError is raised when required column is missing
        with pytest.raises(ValueError):
            Sentence_bank(tmpfilepath)
            
        #----------------------------------------------------------------------
        # Test Case 4: Empty/null values in required columns
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'empty_cells.tsv')
        
        # Create a sentence bank with some empty cells
        empty_cells = pd.DataFrame({
            "Sentence": ["Hola!", "", "¿Qué tal?"],
            "Meaning": ["Hello!", None, "How are you?"],
            "Custom Ratio": [1.0, 0.5, None]
        })
        empty_cells.to_csv(tmpfilepath, sep="\t")
        
        # Initialize and verify that null values are handled correctly
        sentence_bank7 = Sentence_bank(tmpfilepath)
        # Check that no null values remain after processing
        assert not sentence_bank7.sentence_bank.isnull().values.any()
        
        #----------------------------------------------------------------------
        # Test Case 5: Non-numeric values in numeric columns
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'invalid_number.tsv')
        
        # Create a sentence bank with non-numeric value in Custom Ratio
        invalid_number = pd.DataFrame({
            "Sentence": ["Bonjour!"],
            "Meaning": ["Hello!"],
            "Custom Ratio": ["not-a-number"]
        })
        invalid_number.to_csv(tmpfilepath, sep="\t")
        
        # Verify that ValueError is raised for non-numeric values
        with pytest.raises(ValueError):
            Sentence_bank(tmpfilepath)
            
        #----------------------------------------------------------------------
        # Test Case 6: Duplicate sentences
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'duplicate_sentences.tsv')
        
        # Create a sentence bank with duplicate sentences
        duplicate_sentences = pd.DataFrame({
            "Sentence": ["Hola!", "Hola!", "¿Qué tal?"],
            "Meaning": ["Hello!", "Hi!", "How are you?"],
            "Custom Ratio": [1.0, 0.8, 0.5]
        })
        duplicate_sentences.to_csv(tmpfilepath, sep="\t")
        
        # Verify that ValueError is raised for duplicate sentences
        with pytest.raises(ValueError):
            Sentence_bank(tmpfilepath)
            
        #----------------------------------------------------------------------
        # Test Case 7: Extremely long sentences
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'long_sentence.tsv')
        
        # Create a very long sentence (1000 repetitions)
        very_long_text = "Este es un texto extremadamente largo que continúa " * 1000
        long_sentence = pd.DataFrame({
            "Sentence": [very_long_text],
            "Meaning": ["This is an extremely long text that continues..."],
            "Custom Ratio": [1.0]
        })
        long_sentence.to_csv(tmpfilepath, sep="\t")
        
        # Verify that long sentences are handled correctly
        sentence_bank_long = Sentence_bank(tmpfilepath)
        assert sentence_bank_long.sentence_bank.loc[0, "Sentence"] == very_long_text.strip()
        
        #----------------------------------------------------------------------
        # Test Case 8: Extra whitespace handling
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'whitespace.tsv')
        
        # Create sentences with extra whitespace
        whitespace = pd.DataFrame({
            "Sentence": ["  Hola!  ", "¿Qué \t tal?"],
            "Meaning": [" Hello! ", "How are you?"],
            "Custom Ratio": [1.0, 0.5]
        })
        whitespace.to_csv(tmpfilepath, sep="\t")
        
        # Verify that whitespace is handled correctly
        sentence_bank_whitespace = Sentence_bank(tmpfilepath)
        # Check that leading/trailing whitespace is stripped
        assert sentence_bank_whitespace.sentence_bank.loc[0, "Sentence"] == "  Hola!  ".strip()
        # Check that internal whitespace is preserved
        assert sentence_bank_whitespace.sentence_bank.loc[1, "Sentence"] == "¿Qué \t tal?"
        # Check that meaning whitespace is also stripped
        assert sentence_bank_whitespace.sentence_bank.loc[0, "Meaning"] == " Hello! ".strip()
        
        #----------------------------------------------------------------------
        # Test Case 9: Invalid ratio values
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'invalid_ratios.tsv')
        
        # Create a sentence bank with invalid ratio values
        invalid_ratios = pd.DataFrame({
            "Sentence": ["Uno", "Dos", "Tres"],
            "Meaning": ["One", "Two", "Three"],
            "Custom Ratio": [-0.5, 0, 10000]  # Negative, zero, and very large values
        })
        invalid_ratios.to_csv(tmpfilepath, sep="\t")
        
        # Verify that ValueError is raised for invalid ratio values
        with pytest.raises(ValueError, match="Custom Ratios must be between 0 and 1"):
            Sentence_bank(tmpfilepath)
            
        #----------------------------------------------------------------------
        # Test Case 10: Mixed character encodings
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'mixed_encoding.tsv')
        
        # Manually create a file with mixed UTF-8 encodings
        with open(tmpfilepath, 'wb') as f:
            f.write("Sentence\tMeaning\tCustom Ratio\n".encode('utf-8'))
            f.write("こんにちは\tHello\t1.0\n".encode('utf-8'))
            f.write("Здравствуйте\tHello\t0.8\n".encode('utf-8'))
            
        # Verify that non-ASCII characters are handled correctly
        other_encodings = Sentence_bank(tmpfilepath)
        assert other_encodings.sentence_bank.loc[0, "Sentence"] == "こんにちは"
        assert other_encodings.sentence_bank.loc[1, "Sentence"] == "Здравствуйте"
