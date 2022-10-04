"""
Simple example of using the nickname generator.
"""
from src.redcap_record_synthesizer.nickname_and_diminutive_names_lookup import (
    python_parser,
)

if __name__ == "__main__":
    nickname_generator = python_parser.NicknameGenerator()
    test_names = ["Elizabeth", "Charles", "George"]

    for name in test_names:
        nicknames = nickname_generator.get(name)
        print(f"{name} translates to {nicknames}.")
