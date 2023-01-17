"""
Module test_synthesizer.py,
    supports automated testing of FakeRecordGenerator class.

Classes
-------
TestSynthesizer
"""
import pandas
import pytest

from redcap_record_synthesizer.nickname_lookup import python_parser
from redcap_record_synthesizer import FakeRecordGenerator, StateAbbreviationConverter


def test_generator_creation():
    """Test that we can create fake records."""
    #
    # Instantiate the object.
    #
    fake_record_generator = FakeRecordGenerator()

    assert isinstance(fake_record_generator, FakeRecordGenerator)
    #
    # Create records without duplication.
    #
    num_records_desired = 10
    patient_records = fake_record_generator.create_fake_records(
        max_number_copies_of_one_record=0,
        num_records_desired=num_records_desired,
        percent_records_to_duplicate=0,
    )

    assert isinstance(patient_records, pandas.DataFrame)
    assert len(patient_records) == num_records_desired
    #
    # Create records with duplication.
    #
    num_records_desired = 100
    pct_to_duplicate = 10
    patient_records = fake_record_generator.create_fake_records(
        max_number_copies_of_one_record=1,
        num_records_desired=num_records_desired,
        percent_records_to_duplicate=pct_to_duplicate,
    )

    expected_number_of_records = round(
        num_records_desired * (100 + pct_to_duplicate) / 100
    )
    assert isinstance(patient_records, pandas.DataFrame)
    assert len(patient_records) == expected_number_of_records
    #
    # Create records with duplication but all with unique study_ids.
    #
    patient_records = fake_record_generator.create_fake_records(
        duplicate_study_id=False,
        max_number_copies_of_one_record=1,
        num_records_desired=num_records_desired,
        percent_records_to_duplicate=pct_to_duplicate,
    )

    expected_number_of_records = round(
        num_records_desired * (100 + pct_to_duplicate) / 100
    )
    assert isinstance(patient_records, pandas.DataFrame)
    assert len(patient_records) == expected_number_of_records


def test_generator_exceptions():
    """Test that exceptions are raised as expected."""
    #
    # Instantiate the object.
    #
    fake_record_generator = FakeRecordGenerator()

    assert isinstance(fake_record_generator, FakeRecordGenerator)

    # Not an int.
    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            max_number_copies_of_one_record="error",
            num_records_desired=10,
            percent_records_to_duplicate=0,
        )

    # Less than zero.
    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            max_number_copies_of_one_record=-1,
            num_records_desired=10,
            percent_records_to_duplicate=0,
        )

    # Not an int.
    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            max_number_copies_of_one_record=0,
            num_records_desired="error",
            percent_records_to_duplicate=0,
        )

    # Less than zero.
    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            max_number_copies_of_one_record=0,
            num_records_desired=-1,
            percent_records_to_duplicate=0,
        )

    # Not a float.
    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            max_number_copies_of_one_record=0,
            num_records_desired=10,
            percent_records_to_duplicate="error",
        )

    # Less than zero.
    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            max_number_copies_of_one_record=0,
            num_records_desired=10,
            percent_records_to_duplicate=-1,
        )

    # More than 100.
    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            max_number_copies_of_one_record=0,
            num_records_desired=10,
            percent_records_to_duplicate=101,
        )

    # Provide bogus index field name.
    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            index_field_name=1,
            max_number_copies_of_one_record=0,
            num_records_desired=10,
            percent_records_to_duplicate=20,
        )

    with pytest.raises(TypeError):
        fake_record_generator.create_fake_records(
            index_field_name="not a real name",
            max_number_copies_of_one_record=0,
            num_records_desired=10,
            percent_records_to_duplicate=20,
        )


def test_index_column_option():
    fake_record_generator = FakeRecordGenerator()

    assert isinstance(fake_record_generator, FakeRecordGenerator)

    num_records_desired = 10
    patient_records = fake_record_generator.create_fake_records(
        index_field_name="mrn",
        max_number_copies_of_one_record=0,
        num_records_desired=num_records_desired,
        percent_records_to_duplicate=0,
    )

    assert isinstance(patient_records, pandas.DataFrame)
    assert len(patient_records) == num_records_desired


def test_nicknames():
    """Test nickname generation."""
    nickname_generator = python_parser.NicknameGenerator()

    assert isinstance(nickname_generator, python_parser.NicknameGenerator)

    test_name = "Elizabeth"
    nicknames = nickname_generator.get(test_name)
    assert isinstance(nicknames, list)

    assert len(nicknames) >= 2

    expected_nickname = "beth"
    assert expected_nickname in nicknames

    # Expect to receive None.
    assert nickname_generator.get(5) is None
    assert nickname_generator.get("Unobtanium") is None

    # Test expected exceptions.
    with pytest.raises(FileNotFoundError):
        python_parser.NicknameGenerator(filename="not a real file.csv")


def test_state_abbreviations():
    """Test conversion of 'CA' to 'California'."""
    state_abbreviation_converter = StateAbbreviationConverter()

    assert isinstance(
        state_abbreviation_converter, StateAbbreviationConverter
    )

    # One that should translate.
    abbr = "CA"
    full_state_name = state_abbreviation_converter.full_name(abbr)

    assert isinstance(full_state_name, str)
    assert full_state_name == "California"

    # One that should NOT.
    abbr = "XX"
    full_state_name = state_abbreviation_converter.full_name(abbr)

    assert isinstance(full_state_name, str)
    assert full_state_name == abbr


if __name__ == "__main__":  # pragma: no cover
    pass
