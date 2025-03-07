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
        empty = pd.DataFrame({})

        empty.to_csv(tmpfilepath, sep="\t")

        sentence_bank8 = Sentence_bank(tmpfilepath)

        # Verify that empty file creates an empty sentence bank
        assert len(sentence_bank8.sentence_bank) == 0

def test_sentence_bank_creation():

    columns = [
            "Sentence",
            "Meaning",
            "Custom Ratio"
            ]

    with tempfile.TemporaryDirectory() as tempdir:

        # you can e.g. create a file here:
        tmpfilepath = os.path.join(tempdir, 'normal.tsv')

        # create a very basic sentence bank that should word
        normal = pd.DataFrame({
            "Sentence": ["Hola! Como estas?"],
            "Meaning": ["Hello! How are you?"],
            "Custom Ratio": [1.0]
            })

        normal.to_csv(tmpfilepath,sep="\t")

        sentence_bank5 = Sentence_bank(tmpfilepath)

        for column in columns:
            assert column in sentence_bank5.sentence_bank.columns

        # create a path for more_than_nec
        tmpfilepath = os.path.join(tempdir, 'more_than_nec.tsv')

        # create a sentence bank that has more columns than are required
        more_than_nec = pd.DataFrame({
            "Sentence": ["很好，谢谢。"],
            "Pinyin": ["hěn hǎo xièxie"],
            "Meaning": ["Fine, thanks."],
            "HSK average": [1],
            "Custom Ratio": [1]
            })

        more_than_nec.to_csv(tmpfilepath,sep="\t")

        sentence_bank6 = Sentence_bank(tmpfilepath)

        for column in columns:
            assert column in sentence_bank6.sentence_bank.columns


        # test tsv that lacks the correct columns
        # create a path for no meaning
        tmpfilepath = os.path.join(tempdir, 'no_meaning.tsv')

        # create a sentence bank that has more columns than are required
        no_meaning = pd.DataFrame({
            "Sentence": ["很好，谢谢。"],
            "Pinyin": ["hěn hǎo xièxie"],
            "HSK average": [1],
            "Custom Ratio": [1]
            })

        no_meaning.to_csv(tmpfilepath,sep="\t")

        with pytest.raises(ValueError,match=f"Incorrect columns. Expected at least 'Sentence, Meaning, and Custom Ratio', but found {no_meaning.columns}"):
            Sentence_bank(tmpfilepath)


