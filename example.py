"""
Simple example of creating REDCap-like records.
"""
import logging
import sys

from src.redcap_record_synthesizer import fake_records

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    # Set up logging for everything.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)

    logfile_handler = logging.FileHandler(filename="record_deduplicator.log")
    logfile_handler.setLevel(logging.INFO)
    logfile_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logfile_handler.setFormatter(logfile_format)

    logging.basicConfig(
        level=logging.DEBUG, handlers=[console_handler, logfile_handler]
    )

    logger = logging.getLogger(__name__)

    # Synthesize patient records, including duplicates.
    logger.debug("Synthesizing patient records.")
    fake_record_generator = fake_records.FakeRecordGenerator()
    patient_records = fake_record_generator.create_fake_records(
        max_number_copies_of_one_record=3,
        num_records_desired=100,
        percent_records_to_duplicate=5,
    )
