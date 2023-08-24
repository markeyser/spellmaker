import pytest
# tests/test_spellmaker.py
from spellmaker.spellmaker import SpellMaker

@pytest.fixture
def mock_requirements_file(tmp_path):
    """
    Fixture to create a temporary requirements.txt file for testing.

    Parameters
    ----------
    tmp_path : object
        Temporary directory path provided by pytest.

    Returns
    -------
    requirements_path : Path
        Path to the temporary requirements.txt file.
    """
    requirements_content = """
    # This is a comment
    numpy==1.19.2
    pandas==1.2.0
    # This is a comment
    black
    """
    requirements_path = tmp_path / "requirements.txt"
    requirements_path.write_text(requirements_content)
    return requirements_path

def test_get_libraries_from_requirements(mock_requirements_file):
    """
    Test if the `get_libraries_from_requirements` method correctly extracts library names
    from a mock requirements.txt file.
    """
    # Initialize the SpellMaker class with the path to the temporary requirements file
    maker = SpellMaker(requirements_path=mock_requirements_file)

    # Call the method and get the result
    libraries = maker.get_libraries_from_requirements()

    # Assert that the result matches the expected list of libraries
    assert libraries == ['numpy', 'pandas', 'black'], f"Expected ['numpy', 'pandas', 'black'] but got {libraries}"

def test_process_library():
    """
    Test if the `process_library` method correctly extracts terms from a known library.
    """
    maker = SpellMaker()
    library_name = "math"
    
    # Call the method and get the result
    terms = maker.process_library(library_name)
    
    # Assert that the result contains the library name and some known contents
    assert library_name in terms, f"Expected {library_name} in terms but not found"
    assert "sqrt" in terms, "Expected 'sqrt' in terms but not found"  # math.sqrt is a known function
    assert "pi" in terms, "Expected 'pi' in terms but not found"  # math.pi is a known constant

from unittest.mock import patch, Mock

def test_generate_spell_dict(mock_requirements_file, tmp_path):
    """
    Test if the `generate_spell_dict` method correctly generates a spell dictionary
    from a mock requirements.txt file and writes the terms to the specified output path.
    """
    # Initialize the SpellMaker class with the path to the temporary requirements file
    maker = SpellMaker(requirements_path=mock_requirements_file)

    # Define the output path for the generated dictionary
    output_path = tmp_path / "data-science-en.txt"

    # Mock the behavior of the __import__ function to simulate the presence of the libraries
    with patch('builtins.__import__', Mock()):
        # Call the method to generate the spell dictionary
        terms = maker.generate_spell_dict(output_path=output_path)

    # Assert that the result contains the expected terms from the mock requirements.txt
    assert "numpy" in terms, "Expected 'numpy' in terms but not found"
    assert "pandas" in terms, "Expected 'pandas' in terms but not found"
    assert "black" in terms, "Expected 'black' in terms but not found"

def test_write_to_file(tmp_path):
    """
    Test if the `write_to_file` method correctly writes terms to a specified output path.
    """
    maker = SpellMaker()

    # Sample terms to write to the file
    terms = ["numpy", "ndarray", "dot", "pandas", "DataFrame", "read_csv"]

    # Define the output path for the file
    output_path = tmp_path / "data-science-en.txt"

    # Call the method to write terms to the file
    maker.write_to_file(terms, output_path)

    # Read the contents of the written file
    written_content = output_path.read_text().splitlines()

    # Assert that the written content matches the terms
    assert written_content == terms, f"Expected terms {terms} but got {written_content}"

def test_create_spell_dict(mock_requirements_file, tmp_path, capfd):
    """
    Test if the `create_spell_dict` method correctly creates a spell dictionary
    from the mock requirements.txt file and writes the terms to the specified output path.
    """
    # Initialize the SpellMaker class with the path to the temporary requirements file
    maker = SpellMaker(requirements_path=mock_requirements_file)

    # Define the output path for the generated dictionary
    output_path = tmp_path / "data-science-en.txt"

    # Call the method to create the spell dictionary and write to the output file
    maker.create_spell_dict(output_path=output_path)

    # Capture the printed output
    captured = capfd.readouterr()

    # Assert that the warning messages were printed
    assert "Unable to import numpy. Skipping." in captured.out
    assert "Unable to import pandas. Skipping." in captured.out
    assert "Unable to import black. Skipping." in captured.out

