"""
SpellMaker: A Python Package for Generating Custom Spell Check Dictionaries.

This module provides the `SpellMaker` class, which automates the generation
of custom dictionaries for the Code Spell Checker extension in Visual Studio Code.
The primary purpose is to accommodate terms from third-party Python packages 
used in data science projects, ensuring that they are not flagged as spelling errors.

The `SpellMaker` class extracts library names from a given `requirements.txt` file,
processes each library to gather terms, and writes these terms to a specified output file.

Primary Class:
--------------
SpellMaker:
    Methods:
    - get_libraries_from_requirements: Extracts libraries from `requirements.txt`.
    - process_library: Processes a given library to extract terms.
    - generate_spell_dict: Generates a list of terms for all libraries.
    - write_to_file: Writes the terms to the specified output file.
    - create_spell_dict: Main method to generate and write the spell dictionary.

Usage:
------
    >>> spellmaker = SpellMaker()
    >>> spellmaker.create_spell_dict()

Note:
- By default, the class looks for `requirements.txt` in the current directory and 
  writes to `.vscode/dictionaries/data-science-en.txt`.
- Paths can be overridden when initializing the `SpellMaker` class.

"""

class SpellMaker:
    """
    A utility class to generate custom spell check dictionaries for VS Code's Code Spell Checker.

    `SpellMaker` automates the generation of custom dictionaries by extracting 
    terms from third-party Python libraries listed in a `requirements.txt` file. 
    These terms are then written to an output file, making them recognizable by 
    the Code Spell Checker extension in Visual Studio Code.

    Attributes
    ----------
    requirements_path : str
        Path to the `requirements.txt` file containing the list of Python libraries.
        Defaults to "requirements.txt".
    output_path : str
        Path to the output file where the custom dictionary will be saved.
        Defaults to ".vscode/dictionaries/data-science-en.txt".

    Methods
    -------
    get_libraries_from_requirements():
        Extract library names from the specified `requirements.txt` file.
    process_library(library_name: str) -> list:
        Extract terms (like function and class names) from a specified library.
    generate_spell_dict() -> list:
        Generate a comprehensive list of terms from all libraries in `requirements.txt`.
    write_to_file(terms: list):
        Write the collected terms to the specified output file.
    create_spell_dict():
        A wrapper method to generate the spell check dictionary and save it to a file.

    Example
    -------
    >>> maker = SpellMaker()
    >>> maker.create_spell_dict()
    """

    def __init__(self, requirements_path="requirements.txt", output_path=".vscode/dictionaries/data-science-en.txt"):
        """
        Initializes the SpellMaker class with paths for the requirements file and output file.
    
        Parameters
        ----------
        requirements_path : str, optional
            Path to the `requirements.txt` file containing the list of Python libraries.
            Defaults to "requirements.txt".
        output_path : str, optional
            Path to the output file where the custom dictionary will be saved.
            Defaults to ".vscode/dictionaries/data-science-en.txt".
    
        Attributes
        ----------
        requirements_path : str
            Path to the `requirements.txt` file for extracting library names.
        output_path : str
            Path to save the generated custom dictionary.
    
        Example
        -------
        >>> maker = SpellMaker(requirements_path="path/to/requirements.txt", output_path="path/to/output.txt")
        """
        self.requirements_path = requirements_path
        self.output_path = output_path

    def get_libraries_from_requirements(self):
        """
        Extract library names from the specified `requirements.txt` file.
    
        The function reads the `requirements.txt` file line by line. It ignores 
        lines starting with "#" as they are considered comments. For each valid 
        line, it extracts the library name, which is the string before the "=="
        symbol or the last word in case of commands like "pip install".
    
        Returns
        -------
        list
            A list containing names of the libraries mentioned in the 
            `requirements.txt` file.
    
        Raises
        ------
        FileNotFoundError
            If the `requirements.txt` file specified by `requirements_path` 
            attribute is not found.
    
        Example
        -------
        Given a requirements.txt file with content:
        ```
        numpy==1.19.2
        pandas==1.2.0
        pip install mylib==0.1.0
        # This is a comment
        ```
        The function will return:
        ['numpy', 'pandas', 'mylib']
    
        Notes
        -----
        This function assumes the `requirements.txt` file path is set by the 
        `requirements_path` attribute of the `SpellMaker` class.
        """
        libraries = []
        try:
            with open(self.requirements_path, "r") as req:
                for line in req:
                    if not line.startswith("#"):
                        library = line.split("==")[0] if "==" in line else line.split(" ")[-1]
                        libraries.append(library)
        except FileNotFoundError:
            print(f"Error: {self.requirements_path} not found!")
        return libraries

    def process_library(self, library_name):
        """
        Extracts terms (like function and class names) from a specified library.
    
        Parameters
        ----------
        library_name : str
            The name of the library to process.
    
        Returns
        -------
        list
            A list containing the library name and other relevant terms 
            extracted from the library.
    
        Notes
        -----
        If the library is not installed or not found, a warning is printed 
        and an empty list is returned for that library.
        """
        terms = []
        try:
            library = __import__(library_name)
            terms.append(library_name)
            all_library_contents = dir(library)
    
            new_contents = []
    
            # For each item in the library module
            for item in all_library_contents:
                try:
                    # If the item is a class (or a type)
                    if isinstance(getattr(library, item), type):
                        # Get all methods in the class
                        methods = [
                            method
                            for method in dir(getattr(library, item))
                            if not method.startswith("_")
                        ]
                        new_contents.extend(methods)
                except AttributeError:
                    # Skip if attribute doesn't exist
                    continue
    
            all_library_contents.extend(new_contents)
    
            # Remove duplicates from the list
            all_library_contents = list(set(all_library_contents))
    
            # Remove any private attributes or methods (those starting with a `_`)
            all_library_contents = [
                term for term in all_library_contents if not term.startswith("_")
            ]
    
            terms.extend(all_library_contents)
    
        except ImportError:
            print(f"Warning: Unable to import {library_name}. Skipping.")
        
        return terms

    def generate_spell_dict(self):
        """
        Generates a comprehensive list of terms from all libraries listed in the `requirements.txt` file.
    
        The function iterates over each library mentioned in the `requirements.txt` file, 
        processes each library using the `process_library` method, and accumulates 
        all terms, including library names, functions, classes, and methods.
    
        Returns
        -------
        list
            A comprehensive list of terms extracted from all libraries in the 
            `requirements.txt` file. The list might contain duplicates which need 
            to be handled separately.
    
        Notes
        -----
        - The function relies on the `process_library` method to extract terms from each library.
        - Libraries that are not installed or are inaccessible will be skipped, 
          and a warning will be printed.
        - The function assumes that the `requirements.txt` file path is set by the 
          `requirements_path` attribute of the `SpellMaker` class.
    
        Example
        -------
        Given a `requirements.txt` file with content:
        ```
        numpy==1.19.2
        pandas==1.2.0
        ```
        The function might return a list containing terms like:
        ['numpy', 'ndarray', 'dot', 'pandas', 'DataFrame', 'read_csv', ...]
    
        """
        libraries = self.get_libraries_from_requirements()
        all_terms = []
        for library_name in libraries:
            terms = self.process_library(library_name)
            all_terms.extend(terms)
        return all_terms

    def write_to_file(self, terms):
        """
        Writes the collected terms to the specified output file.
    
        This function takes a list of terms and writes each term to a new line 
        in the specified output file. The output file's path is determined by the 
        `output_path` attribute of the `SpellMaker` class.
    
        Parameters
        ----------
        terms : list
            A list of terms (like library names, functions, classes, and methods) 
            to be written to the output file.
    
        Notes
        -----
        - If the specified output directory does not exist, the write operation 
          might fail. Ensure the directory structure exists.
        - This function overwrites the content of the output file if it already exists.
    
        Example
        -------
        Given a list of terms:
        ['numpy', 'ndarray', 'dot', 'pandas', 'DataFrame']
    
        The output file will contain:
        ```
        numpy
        ndarray
        dot
        pandas
        DataFrame
        ```
    
        """
        with open(self.output_path, "w") as f:
            for term in terms:
                f.write(term + "\n")
        print(f"Dictionary generated at {self.output_path}")

    def create_spell_dict(self):
        """
        Generates and writes the custom spell check dictionary to the specified output file.
    
        This is the main method of the `SpellMaker` class. It orchestrates the process 
        of generating a custom dictionary by:
        1. Extracting library names from the `requirements.txt` file.
        2. Processing each library to gather relevant terms.
        3. Writing the accumulated terms to the specified output file.
    
        The paths for the `requirements.txt` file and the output file are determined 
        by the `requirements_path` and `output_path` attributes, respectively.
    
        Notes
        -----
        - The function relies on the `get_libraries_from_requirements`, 
          `process_library`, and `write_to_file` methods for its operation.
        - Any existing content in the output file will be overwritten.
        - If any library listed in the `requirements.txt` is not installed or 
          is inaccessible, it will be skipped and a warning will be printed.
    
        Example
        -------
        >>> maker = SpellMaker()
        >>> maker.create_spell_dict()
        Dictionary generated at .vscode/dictionaries/data-science-en.txt
    
        """
        terms = self.generate_spell_dict()
        self.write_to_file(terms)


if __name__ == '__main__':
    spellmaker = SpellMaker()
    spellmaker.create_spell_dict()
