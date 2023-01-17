[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Pylint](./.github/badges/pylint-badge.svg?dummy=8484744)
![Coverage Status](./.github/badges/coverage-badge.svg?dummy=8484744)
![Last Commit Date](./.github/badges/last-commit-badge.svg?dummy=8484744)

# REDCap Record Synthesizer ![image info](./pictures/groucho_small.png) 
This application uses the [recordlinkage toolkit](https://recordlinkage.readthedocs.io/en/latest/index.html) to generate synthetic REDCap-like records for use in software testing.

## Installation
    pip install git+https://github.com/DBMI/REDCapRecordSynthesizer.git

## Use
From project `redcap_record_synthesizer`, import class `FakeRecordGenerator`:

    from redcap_record_synthesizer import FakeRecordGenerator

Then instantiate an object of the `FakeRecordGenerator` class:

    fake_record_generator = FakeRecordGenerator()

...and call its `create_fake_records` method:

    patient_records = fake_record_generator.create_fake_records()

This method can be customized with these parameters:
* `num_records_desired` How many synthetic patient records do you want to create? [default: 100]
* `percent_records_to_duplicate` To test duplicate-detection software, you might want to inject duplicates of some records. What portion of the records should be duplicated? [default: 3%]
* `max_number_copies_of_one_record` To allow for more than one copy of a given record, set this parameter > 1. [default: 3]
* `index_field_name` Do you want the created Pandas DataFrame to synthesize an index or use an existing variable (like Medical Record Number) as the index? [default: None, meaning its index is synthesized.]
* `duplicate_study_id` Should the duplicate records sometimes use the same study_id values as the original records? [default: True]

## Duplicate records
To be more realistic, the duplicate records aren't *exact* copies of the original. Instead:
* patient's given names are varied from the original ("Bob" instead of "Robert") just as they might be in real data.
* medical record numbers are sometimes regenerated, just as they would be for a patient mistakenly re-enrolled in the database.
* addresses are sometimes changed to use the full state name ("California" instead of "CA")
* the format for date of birth is sometimes changed ("July 01, 2000" instead of "7/1/2000")
* email addresses are sometimes modified to a new provider or format ("first.last" instead of "first_last").
