import os
from pathlib import Path

def test_language_parity():
    """Checks that all languages have all the same files."""

    langs = ["en", "es"]
    templates = Path(os.path.abspath(__file__)).parent.parent / Path("templates")

    prev = None
    for lang in langs:
        file_list = os.listdir(templates / Path(lang))
        if prev is not None:
            print(file_list)
            assert prev == file_list
        prev = file_list


test_language_parity()    