import tempfile
import os
import pytest
import pandas as pd
import re
import time

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

def test_get_sentences_basic_functionality():
    # Use a temporary directory for all test files
    with tempfile.TemporaryDirectory() as tempdir:
        #----------------------------------------------------------------------
        # Test Case 1: Getting a basic valid sentence from the sentence bank
        #----------------------------------------------------------------------
        tmpfilepath = os.path.join(tempdir, 'normal.tsv')
        
        # Create a simple, valid sentence bank
        normal = pd.DataFrame({
            "Sentence": ["Hola! Como estas?","Me gusta queso","Hola Senor"],
            "Meaning": ["Hello! How are you?","I Like Cheese","Hello sir"],
            "Custom Ratio": [1.0, 0.8,0.73]
        })
        normal.to_csv(tmpfilepath, sep="\t")
        
        # Initialize Sentence_bank with the file and verify required columns exist
        sentence_bank_basic = Sentence_bank(tmpfilepath)

        returned_sentences = sentence_bank_basic.get_sentences("Hola",2)

        assert len(returned_sentences) == 2
        assert returned_sentences[0]["Sentence"] == "Hola! Como estas?"
        assert returned_sentences[1]["Sentence"] == "Hola Senor"

def test_get_sentences_empty_inputs():
    #----------------------------------------------------------------------
    # Test Case 2: Testing with empty inputs
    #----------------------------------------------------------------------
    
    # Use a temporary directory for all test files
    with tempfile.TemporaryDirectory() as tempdir:
     
        tmpfilepath = os.path.join(tempdir, 'normal.tsv')
        
        # Create a simple, valid sentence bank
        normal = pd.DataFrame({
            "Sentence": ["Hola! Como estas?","Me gusta queso","Hola Senor"],
            "Meaning": ["Hello! How are you?","I Like Cheese","Hello sir"],
            "Custom Ratio": [1.0, 0.8,0.73]
        })
        normal.to_csv(tmpfilepath, sep="\t")
        
        # Initialize Sentence_bank with the file and verify required columns exist
        sentence_bank_basic = Sentence_bank(tmpfilepath)

        with pytest.raises(ValueError,match="Word must be non-empty string"):
            sentence_bank_basic.get_sentences("",3)

def test_get_sentences_with_invalid_num_sentences():
    # Use a temporary directory for all test files
    with tempfile.TemporaryDirectory() as tempdir:
     
        tmpfilepath = os.path.join(tempdir, 'normal.tsv')
        
        # Create a simple, valid sentence bank
        normal = pd.DataFrame({
            "Sentence": ["Hola! Como estas?","Me gusta queso","Hola Senor"],
            "Meaning": ["Hello! How are you?","I Like Cheese","Hello sir"],
            "Custom Ratio": [1.0, 0.8,0.73]
        })
        normal.to_csv(tmpfilepath, sep="\t")
        
        # Initialize Sentence_bank with the file and verify required columns exist
        sentence_bank_basic = Sentence_bank(tmpfilepath)

        with pytest.raises(ValueError, match=re.escape("Num_sentences must be a int greater than zero and less than len(sentences.tsv)")):
            sentence_bank_basic.get_sentences("Hola",0.5)
        
        with pytest.raises(ValueError, match=re.escape("Num_sentences must be a int greater than zero and less than len(sentences.tsv)")):
            sentence_bank_basic.get_sentences("Hola",-1)

def test_get_sentences_word_position():
    # Test words in middle or end of sentences
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'position.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", "Me gusta queso", "El queso es bueno", "Hasta luego amigo"],
            "Meaning": ["Hello! How are you?", "I Like Cheese", "The cheese is good", "See you later friend"],
            "Custom Ratio": [1.0, 0.8, 0.7, 0.6]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Word in the middle
        middle_results = sentence_bank.get_sentences("gusta", 1)
        assert len(middle_results) == 1
        assert middle_results[0]["Sentence"] == "Me gusta queso"
        
        # Word at the end
        end_results = sentence_bank.get_sentences("queso", 2)
        assert len(end_results) == 2
        assert "Me gusta queso" in [s["Sentence"] for s in end_results]
        assert "El queso es bueno" in [s["Sentence"] for s in end_results]

def test_get_sentences_case_sensitivity():
    # Test case sensitivity handling
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'case.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", "hola amigo", "HOLA MUNDO", "No hola"],
            "Meaning": ["Hello! How are you?", "hello friend", "HELLO WORLD", "Not hello"],
            "Custom Ratio": [1.0, 0.9, 0.8, 0.7]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Test with exact case (assuming case-sensitive matching)
        exact_case_results = sentence_bank.get_sentences("Hola", 4)
        
        # Test with different case (assuming case-insensitive matching)
        different_case_results = sentence_bank.get_sentences("hola", 4)
        
        # Assert based on your implementation's expected behavior
        # If case-sensitive:
        # assert len(exact_case_results) == 1
        # If case-insensitive:
        assert len(exact_case_results) == 4  # Adjust based on your implementation

def test_get_sentences_partial_matches():
    # Test partial word matching behavior
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'partial.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", "Holacuate", "Mexicano", "Holandes"],
            "Meaning": ["Hello! How are you?", "Avocado", "Mexican", "Dutch"],
            "Custom Ratio": [1.0, 0.9, 0.8, 0.7]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Test with partial word "Hola"
        partial_results = sentence_bank.get_sentences("Hola", 3)
        
        # Assert based on your implementation's expected behavior
        # If only exact word matches:
        # assert len(partial_results) == 1
        # If substring matches:
        assert len(partial_results) == 3  # Adjust based on your implementation

def test_get_sentences_more_requested_than_available():
    # Test requesting more matches than exist
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'limited.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", "Me gusta queso", "Hola Senor", "la ceta esta aquia","Hi cabrone"],
            "Meaning": ["Hello! How are you?", "I Like Cheese", "Hello sir", "The mushrooms are here","Hey dude"],
            "Custom Ratio": [1.0, 0.8, 0.73, 0.23, 0.8]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Request more than available
        results = sentence_bank.get_sentences("Hola", 5)
        
        # Should return all available matches without error
        assert len(results) == 2
        assert "Hola! Como estas?" in [s["Sentence"] for s in results]
        assert "Hola Senor" in [s["Sentence"] for s in results]

def test_get_sentences_exceeding_database_size():
    # Test with num_sentences exceeding total database size
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'small.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", "Me gusta queso", "Hola Senor"],
            "Meaning": ["Hello! How are you?", "I Like Cheese", "Hello sir"],
            "Custom Ratio": [1.0, 0.8, 0.73]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Request more than total database size
        with pytest.raises(ValueError, match=r"Num_sentences must be a int greater than zero and less than len\(sentences.tsv\)"):
            sentence_bank.get_sentences("Me", 10)

def test_get_sentences_special_characters():
    # Test with special characters or non-Latin scripts
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'special.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["¿Cómo estás?", "Äpfel sind lecker", "你好，世界", "Привет мир"],
            "Meaning": ["How are you?", "Apples are delicious", "Hello, world", "Hello world"],
            "Custom Ratio": [1.0, 0.9, 0.8, 0.7]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Test with accented character
        accented_results = sentence_bank.get_sentences("Cómo", 1)
        assert len(accented_results) == 1
        
        # Test with non-Latin script
        non_latin_results = sentence_bank.get_sentences("你好", 1)
        assert len(non_latin_results) == 1
        assert non_latin_results[0]["Sentence"] == "你好，世界"

def test_get_sentences_malformed_file():
    # Test with malformed/corrupted input file
    with tempfile.TemporaryDirectory() as tempdir:
        # Test with missing required columns
        missing_col_filepath = os.path.join(tempdir, 'missing_cols.tsv')
        missing_cols = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", "Me gusta queso"],
            # Missing "Meaning" column
            "Custom Ratio": [1.0, 0.8]
        })
        missing_cols.to_csv(missing_col_filepath, sep="\t")
        
        with pytest.raises(Exception):  # Adjust exception type based on your implementation
            Sentence_bank(missing_col_filepath)
        
        # Test with empty file
        empty_filepath = os.path.join(tempdir, 'empty.tsv')
        pd.DataFrame().to_csv(empty_filepath, sep="\t")
        
        with pytest.raises(Exception):  # Adjust exception type based on your implementation
            Sentence_bank(empty_filepath)

def test_get_sentences_large_file():
    # Test with very large input files
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'large.tsv')
        
        # Create a large dataset (1000 sentences)
        sentences = []
        meanings = []
        ratios = []
        
        for i in range(1000):
            if i % 100 == 0:  # Every 100th sentence contains target word
                sentences.append(f"Sentence {i} with target word")
            else:
                sentences.append(f"Sentence {i} without target")
            meanings.append(f"Meaning {i}")
            ratios.append(1.0 - (i/1000))
        
        large_df = pd.DataFrame({
            "Sentence": sentences,
            "Meaning": meanings,
            "Custom Ratio": ratios
        })
        large_df.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Test search performance and accuracy
        start_time = time.time()  # Import time if not already imported
        results = sentence_bank.get_sentences("target", 5)
        end_time = time.time()
        
        assert len(results) == 5
        assert all("target" in s["Sentence"] for s in results)
        
        # Optional performance assertion
        # assert (end_time - start_time) < 1.0  # Should complete in less than 1 second

def test_get_sentences_not_found():
    # Test with search term not found
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'notfound.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", "Me gusta queso", "Hola Senor"],
            "Meaning": ["Hello! How are you?", "I Like Cheese", "Hello sir"],
            "Custom Ratio": [1.0, 0.8, 0.73]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Search for non-existent term
        results = sentence_bank.get_sentences("nonexistent", 2)
        
        # Should return empty list or appropriate indicator
        assert len(results) == 0

def test_get_sentences_regex_patterns():
    # Test regex or special character handling in search terms
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'regex.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", "Hola? Senor", "Hola* is a greeting", "Hola+ amigo"],
            "Meaning": ["Hello! How are you?", "Hello? Sir", "Hola* is a greeting", "Hola+ friend"],
            "Custom Ratio": [1.0, 0.9, 0.8, 0.7]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Test with regex-like patterns
        results_question = sentence_bank.get_sentences("Hola?", 2)
        results_star = sentence_bank.get_sentences("Hola*", 1)
        
        # Assert based on your implementation's expected behavior
        # If treating special chars literally:
        assert len(results_question) > 0
        assert len(results_star) > 0

def test_get_sentences_null_values():
    # Test with null values in the dataframe
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'nulls.tsv')
        
        # Create DataFrame with some null values
        sentences = pd.DataFrame({
            "Sentence": ["Hola! Como estas?", None, "Hola Senor", "Buenos dias"],
            "Meaning": ["Hello! How are you?", "Missing", None, "Good morning"],
            "Custom Ratio": [1.0, None, 0.8, 0.7]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        # Check if initialization handles nulls appropriately
        try:
            sentence_bank = Sentence_bank(tmpfilepath)
            
            # Test search with nulls present
            results = sentence_bank.get_sentences("Hola", 3)
            
            # Should handle nulls gracefully
            assert len(results) > 0
        except Exception as e:
            # If implementation rejects nulls, this is also valid
            assert "null" in str(e).lower() or "nan" in str(e).lower() or "none" in str(e).lower()

def test_get_sentences_sorting_order():
    # Test sorting/priority order
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, 'sorting.tsv')
        
        sentences = pd.DataFrame({
            "Sentence": ["Hola low", "Hola medium", "Hola high", "No match"],
            "Meaning": ["Hello low", "Hello medium", "Hello high", "No match"],
            "Custom Ratio": [0.3, 0.6, 0.9, 0.1]
        })
        sentences.to_csv(tmpfilepath, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath)
        
        # Get results and check order
        results = sentence_bank.get_sentences("Hola", 3)
        
        # Assert they're sorted by Custom Ratio (descending)
        assert len(results) == 3
        assert results[0]["Sentence"] == "Hola high"
        assert results[1]["Sentence"] == "Hola medium"
        assert results[2]["Sentence"] == "Hola low"

def test_rank_sentences_basic_functionality_roman():
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')

        known_words = pd.DataFrame({
            "known": ["Hola","Como","estas"]
            })

        known_words.to_csv(tmpfilepath_known)

        sentences = pd.DataFrame({
            "Sentence": ["Hola, Como estas?"],
            "Meaning": ["Hello, how are you?"],
            "Custom Ratio": [0]
            })

        sentences.to_csv(tmpfilepath_sentences,sep="\t")

        sentence_bank = Sentence_bank(tmpfilepath_sentences)

        sentence_bank.rank_sentences(tmpfilepath_known)

        assert sentence_bank.sentence_bank.loc[0,"Custom Ratio"] == 1

def test_rank_sentences_basic_functionality_hanzi():
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')

        known_words = pd.DataFrame({
            "known": ["你","不","懂"]
            })

        known_words.to_csv(tmpfilepath_known)

        sentences = pd.DataFrame({
            "Sentence": ["你不懂。","你敢！"],
            "Meaning": ["You don't understand", "How dare you?"],
            "Custom Ratio": [0,0]
            })

        sentences.to_csv(tmpfilepath_sentences,sep="\t")

        sentence_bank = Sentence_bank(tmpfilepath_sentences)

        sentence_bank.rank_sentences(tmpfilepath_known)

        assert sentence_bank.sentence_bank.loc[0,"Custom Ratio"] == 1
        assert sentence_bank.sentence_bank.loc[0,"Meaning"] == "You don't understand"
        assert sentence_bank.sentence_bank.loc[0,"Sentence"] == "你不懂。"

        assert sentence_bank.sentence_bank.loc[1,"Custom Ratio"] == 0.5
        assert sentence_bank.sentence_bank.loc[1,"Meaning"] == "How dare you?"
        assert sentence_bank.sentence_bank.loc[1,"Sentence"] == "你敢！"

def test_rank_sentences_empty_known_words():
    """Test when the known words file is empty."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')
        known_words = pd.DataFrame({"known": []})
        known_words.to_csv(tmpfilepath_known)
        
        sentences = pd.DataFrame({
            "Sentence": ["Hello world", "Testing"],
            "Meaning": ["Hello world", "Testing"],
            "Custom Ratio": [0, 0]
        })
        sentences.to_csv(tmpfilepath_sentences, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath_sentences)
        sentence_bank.rank_sentences(tmpfilepath_known)
        
        # All sentences should have ratio 0 as no words are known
        assert sentence_bank.sentence_bank.loc[0, "Custom Ratio"] == 0
        assert sentence_bank.sentence_bank.loc[1, "Custom Ratio"] == 0

def test_rank_sentences_case_sensitivity():
    """Test if the word matching is case-sensitive."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')
        
        known_words = pd.DataFrame({"known": ["hello", "world"]})
        known_words.to_csv(tmpfilepath_known)
        
        sentences = pd.DataFrame({
            "Sentence": ["Hello World", "hello world"],
            "Meaning": ["Greeting", "Greeting lowercase"],
            "Custom Ratio": [0, 0]
        })
        sentences.to_csv(tmpfilepath_sentences, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath_sentences)
        sentence_bank.rank_sentences(tmpfilepath_known)
        
        # Check if case-sensitive (assuming it is)
        # If case-sensitive, first sentence should have ratio 0
        # If case-insensitive, first sentence should have ratio 1
        # Update assertion based on actual implementation
        assert sentence_bank.sentence_bank.loc[1, "Custom Ratio"] == 1

def test_rank_sentences_with_punctuation():
    """Test how punctuation affects word matching."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')
        
        known_words = pd.DataFrame({"known": ["hello", "world"]})
        known_words.to_csv(tmpfilepath_known)
        
        sentences = pd.DataFrame({
            "Sentence": ["Hello, world!", "Hello-world", "Hello...world"],
            "Meaning": ["Greeting with comma", "Greeting with hyphen", "Greeting with ellipsis"],
            "Custom Ratio": [0, 0, 0]
        })
        sentences.to_csv(tmpfilepath_sentences, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath_sentences)
        sentence_bank.rank_sentences(tmpfilepath_known)
        
        # Check how punctuation is handled
        # Assuming the method strips punctuation before matching
        # Update assertions based on actual implementation
        assert all(ratio <= 1.0 for ratio in sentence_bank.sentence_bank["Custom Ratio"])

def test_rank_sentences_with_duplicated_words():
    """Test how repeated words are counted."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')
        
        known_words = pd.DataFrame({"known": ["hello"]})
        known_words.to_csv(tmpfilepath_known)
        
        sentences = pd.DataFrame({
            "Sentence": ["Hello hello hello world"],
            "Meaning": ["Repeated hello"],
            "Custom Ratio": [0]
        })
        sentences.to_csv(tmpfilepath_sentences, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath_sentences)
        sentence_bank.rank_sentences(tmpfilepath_known)
        
        # If each word instance is counted separately, ratio should be 0.75
        # If unique words are counted, ratio should be 0.5
        # Update assertion based on actual implementation
        assert sentence_bank.sentence_bank.loc[0, "Custom Ratio"] == 0.75

def test_rank_sentences_with_different_encodings():
    """Test with different text encodings."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')
        
        known_words = pd.DataFrame({"known": ["café", "résumé"]})
        known_words.to_csv(tmpfilepath_known)
        
        sentences = pd.DataFrame({
            "Sentence": ["Je vais au café", "Mon résumé est prêt"],
            "Meaning": ["I'm going to the cafe", "My resume is ready"],
            "Custom Ratio": [0, 0]
        })
        sentences.to_csv(tmpfilepath_sentences, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath_sentences)
        sentence_bank.rank_sentences(tmpfilepath_known)
        
        # Check if special characters are handled correctly
        assert sentence_bank.sentence_bank.loc[0, "Custom Ratio"] > 0
        assert sentence_bank.sentence_bank.loc[1, "Custom Ratio"] > 0

def test_rank_sentences_with_mixed_languages():
    """Test with sentences containing multiple languages."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')
        
        known_words = pd.DataFrame({"known": ["hello", "hola", "你好"]})
        known_words.to_csv(tmpfilepath_known)
        
        sentences = pd.DataFrame({
            "Sentence": ["Hello and 你好", "Hola y 你好"],
            "Meaning": ["Hello and hello in Chinese", "Hello in Spanish and Chinese"],
            "Custom Ratio": [0, 0]
        })
        sentences.to_csv(tmpfilepath_sentences, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath_sentences)
        sentence_bank.rank_sentences(tmpfilepath_known)
        
        # Check if mixed languages are handled correctly
        assert sentence_bank.sentence_bank.loc[0, "Custom Ratio"] > 0
        assert sentence_bank.sentence_bank.loc[1, "Custom Ratio"] > 0

def test_rank_sentences_with_very_long_sentence():
    """Test with an extremely long sentence."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')
        
        known_words = pd.DataFrame({"known": ["hello", "world"]})
        known_words.to_csv(tmpfilepath_known)
        
        # Create a very long sentence
        long_sentence = "hello " + " ".join(["word"] * 1000) + " world"
        
        sentences = pd.DataFrame({
            "Sentence": [long_sentence],
            "Meaning": ["Very long sentence"],
            "Custom Ratio": [0]
        })
        sentences.to_csv(tmpfilepath_sentences, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath_sentences)
        sentence_bank.rank_sentences(tmpfilepath_known)
        
        # Check if long sentences are handled without issues
        assert 0 <= sentence_bank.sentence_bank.loc[0, "Custom Ratio"] <= 1.0

def test_rank_sentences_with_whitespace_only():
    """Test with whitespace-only sentences."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath_known = os.path.join(tempdir, 'known.tsv')
        tmpfilepath_sentences = os.path.join(tempdir, 'sentences.tsv')
        
        known_words = pd.DataFrame({"known": ["hello"]})
        known_words.to_csv(tmpfilepath_known)
        
        sentences = pd.DataFrame({
            "Sentence": ["   ", "t\t\n"],
            "Meaning": ["Spaces only", "Tab and newline"],
            "Custom Ratio": [0, 0]
        })
        sentences.to_csv(tmpfilepath_sentences, sep="\t")
        
        sentence_bank = Sentence_bank(tmpfilepath_sentences)
        sentence_bank.rank_sentences(tmpfilepath_known)
        
        # Empty sentences should have ratio 0
        assert sentence_bank.sentence_bank.loc[0, "Custom Ratio"] == 0
        assert sentence_bank.sentence_bank.loc[1, "Custom Ratio"] == 0


def test_add_sentence():
    pass
