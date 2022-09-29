"""
Module test_synthesizer.py, which supports automated testing of FakeRecordGenerator class.

Classes
-------
TestSynthesizer
"""
import pandas
import unittest

from dbmi_synthesizer import fake_records
from dbmi_synthesizer.nickname_and_diminutive_names_lookup import python_parser
from dbmi_synthesizer import state_abbr_conversion


class TestSynthesizer(unittest.TestCase):
    """
    Class used for testing FakeRecordGenerator class.

    Attributes
    ----------

    Methods
    -------

    """

    def test_generator_creation(self):
        """Test that we can create fake records."""
        #
        # Instantiate the object.
        #
        fake_record_generator = fake_records.FakeRecordGenerator()

        self.assertIsInstance(
            fake_record_generator,
            fake_records.FakeRecordGenerator,
            "Unable to instantiate FakeRecordGenerator object.",
        )
        #
        # Create records without duplication.
        #
        num_records_desired = 10
        patient_records = fake_record_generator.create_fake_records(
            max_number_copies_of_one_record=0,
            num_records_desired=num_records_desired,
            percent_records_to_duplicate=0,
        )

        self.assertIsInstance(
            patient_records, pandas.DataFrame, "Unable to create fake records."
        )
        self.assertEqual(
            len(patient_records),
            num_records_desired,
            f"Created {len(patient_records)} instead of {num_records_desired} of records.",
        )
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
        self.assertIsInstance(
            patient_records, pandas.DataFrame, "Unable to create fake records."
        )
        self.assertEqual(
            len(patient_records),
            expected_number_of_records,
            "Created {len(patient_records)} instead of {expected_number_of_records} of records.",
        )

    def test_generator_exceptions(self):
        """Test that exceptions are raised as expected."""
        #
        # Instantiate the object.
        #
        fake_record_generator = fake_records.FakeRecordGenerator()

        self.assertIsInstance(
            fake_record_generator,
            fake_records.FakeRecordGenerator,
            "Unable to instantiate FakeRecordGenerator object.",
        )

        # Not an int.
        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                max_number_copies_of_one_record="error",
                num_records_desired=10,
                percent_records_to_duplicate=0,
            )

        # Less than zero.
        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                max_number_copies_of_one_record=-1,
                num_records_desired=10,
                percent_records_to_duplicate=0,
            )

        # Not an int.
        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                max_number_copies_of_one_record=0,
                num_records_desired="error",
                percent_records_to_duplicate=0,
            )

        # Less than zero.
        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                max_number_copies_of_one_record=0,
                num_records_desired=-1,
                percent_records_to_duplicate=0,
            )

        # Not a float.
        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                max_number_copies_of_one_record=0,
                num_records_desired=10,
                percent_records_to_duplicate="error",
            )

        # Less than zero.
        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                max_number_copies_of_one_record=0,
                num_records_desired=10,
                percent_records_to_duplicate=-1,
            )

        # More than 100.
        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                max_number_copies_of_one_record=0,
                num_records_desired=10,
                percent_records_to_duplicate=101,
            )

        # Provide bogus index field name.
        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                index_field_name=1,
                max_number_copies_of_one_record=0,
                num_records_desired=10,
                percent_records_to_duplicate=20,
            )

        with self.assertRaises(TypeError):
            fake_record_generator.create_fake_records(
                index_field_name="not a real name",
                max_number_copies_of_one_record=0,
                num_records_desired=10,
                percent_records_to_duplicate=20,
            )

    def test_index_column_option(self):
        fake_record_generator = fake_records.FakeRecordGenerator()

        self.assertIsInstance(
            fake_record_generator,
            fake_records.FakeRecordGenerator,
            "Unable to instantiate FakeRecordGenerator object.",
        )

        num_records_desired=10
        patient_records = fake_record_generator.create_fake_records(
            index_field_name="mrn",
            max_number_copies_of_one_record=0,
            num_records_desired=num_records_desired,
            percent_records_to_duplicate=0,
        )

        self.assertIsInstance(
            patient_records, pandas.DataFrame, "Unable to create fake records."
        )
        self.assertEqual(
            len(patient_records),
            num_records_desired,
            "Created {len(patient_records)} instead of {num_records_desired} of records.",
        )

    def test_nicknames(self):
        """Test nickname generation."""
        nickname_generator = python_parser.NicknameGenerator()

        self.assertIsInstance(
            nickname_generator,
            python_parser.NicknameGenerator,
            "Unable to instantiate NicknameGenerator object.",
        )

        test_name = "Elizabeth"
        nicknames = nickname_generator.get(test_name)
        self.assertIsInstance(
            nicknames,
            list,
            "Unable to retrieve nicknames for '" + test_name + "'.",
        )

        self.assertGreaterEqual(
            len(nicknames),
            2,
            "Didn't retrieve a list of nicknames for '" + test_name + "'.",
        )
        expected_nickname = "beth"
        self.assertTrue(
            expected_nickname in nicknames,
            "Didn't find '"
            + expected_nickname
            + "' in nicknames for '"
            + test_name
            + "'.",
        )

        # Expect to receive None.
        self.assertIsNone(
            nickname_generator.get(5),
            "Did not expect to receive an answer from non-string input.",
        )
        self.assertIsNone(
            nickname_generator.get("Unobtanium"),
            "Did not expect to receive an answer from non-name.",
        )

        # Test expected exceptions.
        with self.assertRaises(FileNotFoundError):
            python_parser.NicknameGenerator(filename="not a real file.csv")

    def test_state_abbreviations(self):
        """Test conversion of 'CA' to 'California'."""
        state_abbreviation_converter = (
            state_abbr_conversion.StateAbbreviationConverter()
        )

        self.assertIsInstance(
            state_abbreviation_converter,
            state_abbr_conversion.StateAbbreviationConverter,
            "Unable to instantiate StateAbbreviationConverter object.",
        )

        # One that should translate.
        abbr = "CA"
        full_state_name = state_abbreviation_converter.full_name(abbr)

        self.assertIsInstance(
            full_state_name,
            str,
            "Unable to convert '" + abbr + "' to full state name.",
        )
        self.assertEqual(
            full_state_name,
            "California",
            "Unable to correctly convert '" + abbr + "' to full state name.",
        )

        # One that should NOT.
        abbr = "XX"
        full_state_name = state_abbreviation_converter.full_name(abbr)

        self.assertIsInstance(
            full_state_name,
            str,
            "Unable to convert '" + abbr + "' to full state name.",
        )
        self.assertEqual(
            full_state_name,
            abbr,
            "Unable to correctly convert '" + abbr + "' to full state name.",
        )


if __name__ == "__main__":  # pragma: no cover
    pass
