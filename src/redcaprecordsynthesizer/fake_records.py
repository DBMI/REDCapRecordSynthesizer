"""
Module: contains class FakeRecordGenerator,
which generates synthetic REDCap-like records.
"""
import logging
import random
import re
from datetime import datetime, timedelta
from typing import Union

import pandas  # type: ignore[import]
from faker import Faker  # type: ignore[import]

from redcaprecordsynthesizer.nickname_lookup.python_parser import (
    NicknameGenerator,  # type: ignore[import]
)
from redcaprecordsynthesizer.state_abbr_conversion import (
    StateAbbreviationConverter,  # type: ignore[import]
)


class FakeRecordGenerator:  # pylint: disable=logging-fstring-interpolation,
    # too-many-locals
    """
    Synthesize realistic patient records.

    ...

    Attributes
    ----------
    no public attributes

    Methods
    -------
    create_fake_records(index_field_name,
                        duplicate_study_id,
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
        self.__duplicate_study_id = True
        self.__existing_study_ids = []

    def __check_index_field_name(self, index_field_name: str) -> None:
        if not isinstance(index_field_name, str):  # It's OK if it's zero-length.
            self.__log.error("Input 'index_field_name' is not a str.")
            raise TypeError("Input 'index_field_name' is not a str.")

    def __check_max_number_copies_of_one_record(
        self, max_number_copies_of_one_record: int
    ) -> None:
        if not isinstance(max_number_copies_of_one_record, int):
            self.__log.error(
                "Input 'max_number_copies_of_one_record' " "is not an int."
            )
            raise TypeError("Input 'max_number_copies_of_one_record' " "is not an int.")

        if max_number_copies_of_one_record < 0:
            self.__log.error("Input 'max_number_copies_of_one_record' " "is < 0.")
            raise TypeError("Input 'max_number_copies_of_one_record' " "is < 0>.")

    def __check_num_records_desired(self, num_records_desired: int) -> None:
        if not isinstance(num_records_desired, int):
            self.__log.error("Input 'num_records_desired' " "is not an int.")
            raise TypeError("Input 'num_records_desired' " "is not an int.")

        if num_records_desired <= 0:
            self.__log.error("Input 'num_records_desired' " "is not a positive int.")
            raise TypeError("Input 'num_records_desired' " "is not a positive int.")

    def __check_percent_records_to_duplicate(
        self, percent_records_to_duplicate: Union[int, float]
    ) -> None:
        if not isinstance(percent_records_to_duplicate, float):
            self.__log.error("Input 'percent_records_to_duplicate' " "is not an float.")
            raise TypeError("Input 'percent_records_to_duplicate' " "is not an float.")

        if not 0 <= percent_records_to_duplicate <= 100:
            self.__log.error(
                "Input 'percent_records_to_duplicate' " "is not between 0 and 100."
            )
            raise TypeError(
                "Input 'percent_records_to_duplicate' " "is not between 0 and 100."
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
            "Synthesizing email address for {given_name} {surname}.",
            extra={"given_name": given_name, "surname": surname},
        )  # pragma: no cover

        # Is the email given.surname or given_surname or givensurname?
        name_dividers = [".", "_", ""]
        name_divider = name_dividers[random.randrange(0, len(name_dividers))]

        if random.uniform(0, 1) <= probability_of_using_first_initial_only:
            given_name_used = given_name[0]
            self.__log.debug(
                "Only using the first initial {given_name_used}.",
                extra={"given_name_used": given_name_used},
            )

        new_address = (
            given_name_used.lower()
            + name_divider
            + surname.lower()
            + "@"
            + fake.free_email_domain()
        )
        self.__log.debug(
            "Synthesized: {new_address}.", extra={"new_address": new_address}
        )
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

        # Ensure that primary consent is simulated
        # to have been given when over 18.
        eighteen_years = timedelta(days=365.25 * 18)
        primary_consent_date = fake.date_between(birthdate + eighteen_years)
        core_participant_date = fake.date_between(primary_consent_date)

        # Exclude territories (like the Virgin Islands) because
        # methods postalcode_in_state and zipcode_in_state
        # can't handle territories.
        state_abbr = fake.state_abbr(include_territories=False)

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
        duplicate_study_id: bool = True,
        index_field_name: str = "",
        max_number_copies_of_one_record: int = 3,
        num_records_desired: int = 100,
        percent_records_to_duplicate: float = 3.0,
    ) -> pandas.DataFrame:
        """Synthesize a whole set of patient records,
        including duplicates, errors, etc.

        Parameters
        ----------
        duplicate_study_id : bool
            Optional. Do you want to allow
            duplicate records to have the same study id?
            Default : True
        index_field_name : str
            Optional. Specify if one of the record columns should
            be used instead of a synthetic index. Default: empty string
        max_number_copies_of_one_record : int
            Optional. Number of copies to be made of any one record.
            Default: 3
        num_records_desired : int
            Optional. Number of patient records to be created.
            Default: 100
        percent_records_to_duplicate : float or int
            Optional. The % of the records that should be duplicated.
            Default: 3%

        Raises
        ------
        TypeError
            If inputs not the required types.

        Returns
        -------
        pandas DataFrame
        """
        self.__duplicate_study_id = duplicate_study_id
        self.__check_index_field_name(index_field_name=index_field_name)
        self.__check_max_number_copies_of_one_record(
            max_number_copies_of_one_record=max_number_copies_of_one_record
        )
        self.__check_num_records_desired(num_records_desired=num_records_desired)

        if isinstance(percent_records_to_duplicate, int):
            percent_records_to_duplicate = percent_records_to_duplicate * 1.0

        self.__check_percent_records_to_duplicate(
            percent_records_to_duplicate=percent_records_to_duplicate
        )

        # To ensure study ids are unique, we'll generate them here all at once.
        study_ids = random.sample(self.__range_study_id, k=num_records_desired)

        self.__log.info(
            "Generating {num_records_desired} synthetic patient records.",
            extra={"num_records_desired": num_records_desired},
        )
        records = self.__initialize_fake_records(
            num_records_desired=num_records_desired, study_ids=study_ids
        )

        # Initialize our list of all the study_ids used so far.
        self.__existing_study_ids = records["study_id"].to_numpy().tolist()

        # Duplicate some rows.
        num_records_to_duplicate = int(
            round(num_records_desired * percent_records_to_duplicate / 100.0)
        )
        self.__log.info(
            "Selecting {num_records_to_duplicate} records to duplicate.",
            extra={"num_records_to_duplicate": num_records_to_duplicate},
        )
        nickname_generator = NicknameGenerator()
        state_abbreviation_converter = StateAbbreviationConverter()

        for _ in range(num_records_to_duplicate):
            # Grab a record at random.
            # (sri ==> "selected record index")
            sri = random.randrange(start=0, stop=num_records_desired)
            selected_record = records.loc[sri]  # type: ignore[call-overload]
            set_of_nicknames = nickname_generator.get(
                name=selected_record["first_name"]
            )
            full_state_name = state_abbreviation_converter.full_name(
                two_letter_code=selected_record["state"]
            )

            # Maybe we're asked to create MORE than one duplicate.
            num_copies_of_this_record = 1

            if max_number_copies_of_one_record > 0:
                num_copies_of_this_record = random.randrange(
                    start=1, stop=max_number_copies_of_one_record + 1
                )

            self.__log.info(
                ".Making {num_copies} copies of this record.",
                extra={"num_copies": num_copies_of_this_record},
            )

            for _ in range(num_copies_of_this_record):
                # Make a copy & assign it a unique index.
                record_copy = records.xs(key=sri)  # type: ignore[operator]
                record_copy.name = len(records)
                mrn_list = list(records["mrn"])

                record_copy = self.__duplicate_record(
                    record=record_copy,
                    medical_record_numbers=mrn_list,
                    nicknames=set_of_nicknames,
                    state_name=full_state_name,
                )

                # Insert this copy into records.
                records = records.append(record_copy)

        # If specified, set the desired field as the index.
        if len(index_field_name) > 0:
            if index_field_name not in records.columns:
                self.__log.exception(
                    "Field '{field_name}' is not present "
                    "in the 'records' DataFrame.",
                    extra={"field_name": index_field_name},
                )
                raise TypeError(
                    f"Field {index_field_name} is not present "
                    f"in the 'records' DataFrame."
                )

            records.set_index(index_field_name, inplace=True)  # type: ignore[call-arg]

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
        self,
        record: pandas.DataFrame,
        medical_record_numbers: list,
        nicknames: list,
        state_name: str,
    ) -> pandas.DataFrame:
        date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%B %d, %Y", "%b %d, %Y"]
        probability_of_duplicating_study_id = 0.0

        if self.__duplicate_study_id:
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

        # Simulate the kind of differences that might occur
        # if a user were to be re-added:
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

        #   2) Sometimes use the full state name
        #   instead of the postal abbreviation.
        if random.uniform(0, 1) <= probability_of_using_full_state_name:
            record["state"] = state_name

        #   3) Enter date of birth in a different format.
        birthdate = datetime.strptime(str(record["dob"]), "%Y-%m-%d")
        this_date_format = date_formats[random.randrange(0, len(date_formats))]
        record["dob"] = birthdate.strftime(this_date_format)

        #   4) People might change their email provider.
        given_name = str(record["first_name"])
        surname = str(record["last_name"])
        record["email_address"] = self.__create_fake_email_address(
            given_name=given_name, surname=surname
        )

        #   5) Maybe the patient was entered under a new MRN.
        if random.uniform(0, 1) <= probability_of_new_mrn:
            record["mrn"] = max(medical_record_numbers) + 1

        return record

    def __initialize_fake_records(
        self, num_records_desired: int, study_ids: list
    ) -> pandas.DataFrame:

        records = pandas.DataFrame()
        self.__log.info(
            "Generating {num_records} synthetic patient records.",
            extra={"num_records": num_records_desired},
        )
        pandas.options.mode.chained_assignment = None

        for record_number in range(num_records_desired):
            study_id = study_ids[record_number]
            new_record = self.__create_fake_record(next_study_id=study_id)
            new_df = pandas.DataFrame(data=new_record, index=[record_number])

            if len(records) == 0:
                records = new_df
            else:
                records = records.append(new_df)

        return records


if __name__ == "__main__":  # pragma: no cover
    fake_records_object = FakeRecordGenerator()
