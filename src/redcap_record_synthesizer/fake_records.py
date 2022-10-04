"""
Module: contains class FakeRecordGenerator, which generates synthetic REDCap-like records.
"""
import logging
import random
import re
import typing

from datetime import datetime, timedelta

import pandas as pd

from faker import Faker
from src.redcap_record_synthesizer.nickname_and_diminutive_names_lookup import (
    python_parser,
)
from src.redcap_record_synthesizer import state_abbr_conversion


class FakeRecordGenerator:  # pylint: disable=logging-fstring-interpolation, too-many-locals
    """
    Synthesize realistic patient records.

    ...

    Attributes
    ----------
    no public attributes

    Methods
    -------
    create_fake_records(index_field_name,
                        max_number_copies_of_one_record,
                        num_records_desired,
                        percent_records_to_duplicate)
        Create a DataFrame of synthetic patient records.
    create_fake_study_id()
        Synthesize a new record index.
    """

    def __init__(self):
        self.__log = logging.getLogger(__name__)
        min_study_id = 10000
        max_study_id = 99999
        self.__range_study_id = range(min_study_id, max_study_id)
        self.__existing_study_ids = []

    def __check_index_field_name(self, index_field_name: str) -> None:
        if index_field_name is not None and not isinstance(index_field_name, str):
            self.__log.error("Input 'index_field_name' is not a str.")
            raise TypeError("Input 'index_field_name' is not a str.")

    def __check_max_number_copies_of_one_record(
        self, max_number_copies_of_one_record: int
    ) -> None:
        if not isinstance(max_number_copies_of_one_record, int):
            self.__log.error("Input 'max_number_copies_of_one_record' is not an int.")
            raise TypeError("Input 'max_number_copies_of_one_record' is not an int.")

        if max_number_copies_of_one_record < 0:
            self.__log.error("Input 'max_number_copies_of_one_record' is < 0.")
            raise TypeError("Input 'max_number_copies_of_one_record' is < 0>.")

    def __check_num_records_desired(self, num_records_desired: int) -> None:
        if not isinstance(num_records_desired, int):
            self.__log.error("Input 'num_records_desired' is not an int.")
            raise TypeError("Input 'num_records_desired' is not an int.")

        if num_records_desired <= 0:
            self.__log.error("Input 'num_records_desired' is not a positive int.")
            raise TypeError("Input 'num_records_desired' is not a positive int.")

    def __check_percent_records_to_duplicate(
        self, percent_records_to_duplicate: typing.Union[int, float]
    ) -> None:
        if not isinstance(percent_records_to_duplicate, float):
            self.__log.error("Input 'percent_records_to_duplicate' is not an float.")
            raise TypeError("Input 'percent_records_to_duplicate' is not an float.")

        if not 0 <= percent_records_to_duplicate <= 100:
            self.__log.error(
                "Input 'percent_records_to_duplicate' is not between 0 and 100."
            )
            raise TypeError(
                "Input 'percent_records_to_duplicate' is not between 0 and 100."
            )

    def __create_fake_email_address(self, given_name: str, surname: str) -> str:
        """Create a realistic email address.

        Parameters
        ----------
        given_name : str
        surname : str

        Raises
        ------
        TypeError
            If inputs are not the required types.

        Returns
        -------
        str
        """
        fake = Faker()
        given_name_used = given_name
        probability_of_using_first_initial_only = 0.25

        if not isinstance(given_name, str):  # pragma: no cover
            self.__log.error("Input 'given_name' is not a str.")
            raise TypeError("Input 'given_name' is not a str.")

        if not isinstance(surname, str):  # pragma: no cover
            self.__log.error("Input 'surname' is not a str.")
            raise TypeError("Input 'surname' is not a str.")

        self.__log.debug(
            f"Synthesizing email address for {given_name} {surname}."
        )  # pragma: no cover

        # Is the email given.surname or given_surname or givensurname?
        name_dividers = [".", "_", ""]
        name_divider = name_dividers[random.randrange(0, len(name_dividers))]

        if random.uniform(0, 1) <= probability_of_using_first_initial_only:
            given_name_used = given_name[0]
            self.__log.debug(f"Only using the first initial {given_name_used}.")

        new_address = (
            given_name_used.lower()
            + name_divider
            + surname.lower()
            + "@"
            + fake.free_email_domain()
        )
        self.__log.debug(f"Synthesized: {new_address}.")
        return new_address

    def __create_fake_record(self, next_study_id: int) -> dict:
        """Synthesize one record for testing.

        Parameters
        ---------
        next_study_id :   int

        Raises
        ------
        TypeError
            If input not the required type.

        Return
        ------
        dict
        """
        if not isinstance(next_study_id, int):  # pragma: no cover
            self.__log.error("Input 'next_study_id' is not an int.")
            raise TypeError("Input 'next_study_id' is not an int.")

        fake = Faker()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=115)

        # Ensure that primary consent is simulated to have been given when over 18.
        eighteen_years = timedelta(days=365.25 * 18)
        primary_consent_date = fake.date_between(birthdate + eighteen_years)
        core_participant_date = fake.date_between(primary_consent_date)
        state_abbr = fake.state_abbr()

        # Strip off the extension.
        phone_number = fake.phone_number()
        phone_number = re.sub(r"x\d+", "", phone_number)

        # We'll want the names available for email address.
        given_name = fake.first_name()
        surname = fake.last_name()

        record = {
            "study_id": next_study_id,
            "first_name": given_name,
            "last_name": surname,
            "phone_number": phone_number,
            "email_address": self.__create_fake_email_address(given_name, surname),
            "street_address_line_1": fake.street_address(),
            "city": fake.city(),
            "state": state_abbr,
            "zip_code": fake.zipcode_in_state(state_abbr),
            "mrn": fake.random_int(min=100000, max=999999),
            "dob": birthdate.strftime("%Y-%m-%d"),
            "ethnicity": fake.random_int(min=1, max=2),
            "race": fake.random_int(min=1, max=5),
            "sex": fake.random_int(min=1, max=3),
            "core_participant_date": core_participant_date.strftime("%Y-%m-%d"),
            "primary_consent_date": primary_consent_date.strftime("%Y-%m-%d"),
            "date_of_last_activity": datetime.now().strftime("%Y-%m-%d"),
        }

        return record

    def create_fake_records(
        self,
        index_field_name: str = None,
        max_number_copies_of_one_record: int = 3,
        num_records_desired: int = 100,
        percent_records_to_duplicate: float = 3.0,
    ) -> pd.DataFrame:
        """Synthesize a whole set of patient records, including duplicates, errors, etc.

        Parameters
        ----------
        index_field_name : str
            Optional. Specify if one of the record columns should
            be used instead of a synthetic index. Default: None
        max_number_copies_of_one_record : int
            Optional. Number of copies to be made of any one record. Default: 3
        num_records_desired : int
            Optional. Number of patient records to be created. Default: 100
        percent_records_to_duplicate : float or int
            Optional. The % of the records that should be duplicated. Default: 3%

        Raises
        ------
        TypeError
            If inputs not the required types.

        Returns
        -------
        pandas DataFrame
        """
        self.__check_index_field_name(index_field_name)
        self.__check_max_number_copies_of_one_record(max_number_copies_of_one_record)
        self.__check_num_records_desired(num_records_desired)

        if isinstance(percent_records_to_duplicate, int):
            percent_records_to_duplicate = percent_records_to_duplicate * 1.0

        self.__check_percent_records_to_duplicate(percent_records_to_duplicate)

        # To ensure study ids are unique, we'll generate them here all at once.
        study_ids = random.sample(self.__range_study_id, num_records_desired)

        self.__log.info(f"Generating {num_records_desired} synthetic patient records.")
        records = self.__initialize_fake_records(num_records_desired, study_ids)

        # Initialize our list of all the study_ids used so far.
        self.__existing_study_ids = records["study_id"].to_numpy().tolist()

        # Duplicate some rows.
        num_records_to_duplicate = int(
            round(num_records_desired * percent_records_to_duplicate / 100.0)
        )
        self.__log.info(f"Selecting {num_records_to_duplicate} records to duplicate.")
        nickname_generator = python_parser.NicknameGenerator()
        state_abbreviation_converter = (
            state_abbr_conversion.StateAbbreviationConverter()
        )

        for _ in range(num_records_to_duplicate):
            # Grab a record at random.
            selected_record_index = random.randrange(0, num_records_desired)
            selected_record = records.loc[selected_record_index]
            set_of_nicknames = nickname_generator.get(selected_record["first_name"])
            full_state_name = state_abbreviation_converter.full_name(
                selected_record["state"]
            )

            # Maybe we're asked to create MORE than one duplicate.
            num_copies_of_this_record = 1

            if max_number_copies_of_one_record > 0:
                num_copies_of_this_record = random.randrange(
                    1, max_number_copies_of_one_record + 1
                )

            self.__log.info(
                f".Making {num_copies_of_this_record} copies of this record."
            )

            for _ in range(num_copies_of_this_record):
                # Make a copy & assign it a unique index.
                record_copy = records.xs(selected_record_index)
                record_copy.name = len(records)
                mrn_list = records["mrn"]

                record_copy = self.__duplicate_record(
                    record=record_copy,
                    mrns=mrn_list,
                    nicknames=set_of_nicknames,
                    state_name=full_state_name,
                )

                # Insert this copy into records.
                records = records.append(record_copy)

        # If specified, set the desired field as the index.
        if index_field_name is not None:
            if index_field_name not in records.columns:
                self.__log.error(
                    f"Field {index_field_name} is not present in the 'records' DataFrame."
                )
                raise TypeError(
                    f"Field {index_field_name} is not present in the 'records' DataFrame."
                )

            records.set_index(index_field_name, inplace=True)

        return records

    def create_fake_study_id(self) -> int:
        """Synthesize one unused index number.

        Returns
        -------
        int
        """
        new_study_id = random.choice(
            [x for x in self.__range_study_id if x not in self.__existing_study_ids]
        )

        self.__existing_study_ids.append(new_study_id)
        return new_study_id

    def __duplicate_record(
        self, record: pd.DataFrame, mrns: list, nicknames: list, state_name: str
    ) -> pd.DataFrame:
        date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%B %d, %Y", "%b %d, %Y"]
        probability_of_duplicating_study_id = 0.20
        probability_of_new_mrn = 0.20
        probability_of_using_full_state_name = 0.33
        probability_of_using_nickname = 0.33

        # Do we generate a unique study_id or keep the existing one?
        #  (which will result in duplicate study_id values across the dataFrame.)
        # Normally we test for < probability, not >.
        # But here, creating a unique study_id is what we do when
        # the probability test fails.
        if random.uniform(0, 1) >= probability_of_duplicating_study_id:
            record["study_id"] = self.create_fake_study_id()

        # Simulate the kind of differences that might occur if a user were to be re-added:
        #   1) Use a nickname instead of the user's first_name.
        if (
            nicknames is not None
            and len(nicknames) > 0
            and random.uniform(0, 1) < probability_of_using_nickname
        ):
            # Each time we "pop()" we will get a different nickname.
            # (Make sure it's not emptied out.)
            try:
                random_nickname = nicknames.pop().title()
                record["first_name"] = random_nickname
            except KeyError:  # pragma: no cover
                # We're out of nicknames; keep the original name.
                pass

        #   2) Sometimes use the full state name instead of the postal abbreviation.
        if random.uniform(0, 1) <= probability_of_using_full_state_name:
            record["state"] = state_name

        #   3) Enter date of birth in a different format.
        birthdate = datetime.strptime(record["dob"], "%Y-%m-%d")
        this_date_format = date_formats[random.randrange(0, len(date_formats))]
        record["dob"] = birthdate.strftime(this_date_format)

        #   4) People might change their email provider.
        given_name = record["first_name"]
        surname = record["last_name"]
        record["email_address"] = self.__create_fake_email_address(given_name, surname)

        #   5) Maybe the patient was entered under a new MRN.
        if random.uniform(0, 1) <= probability_of_new_mrn:
            record["mrn"] = max(mrns) + 1

        return record

    def __initialize_fake_records(
        self, num_records_desired: int, study_ids: list
    ) -> pd.DataFrame:
        records = None
        self.__log.info(f"Generating {num_records_desired} synthetic patient records.")
        pd.options.mode.chained_assignment = None

        for record_number in range(num_records_desired):
            study_id = study_ids[record_number]
            new_record = self.__create_fake_record(study_id)
            new_df = pd.DataFrame(new_record, index=[record_number])

            if records is None:
                records = new_df
            else:
                records = records.append(new_df)

        return records


if __name__ == "__main__":  # pragma: no cover
    fake_records_object = FakeRecordGenerator()
