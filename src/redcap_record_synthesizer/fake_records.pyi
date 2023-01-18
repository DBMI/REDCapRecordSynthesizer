import pandas

class FakeRecordGenerator:
    def __init__(self) -> None: ...
    def create_fake_records(
        self,
        index_field_name: str = ...,
        max_number_copies_of_one_record: int = ...,
        num_records_desired: int = ...,
        percent_records_to_duplicate: float = ...,
    ) -> pandas.DataFrame: ...
    def create_fake_study_id(self) -> int: ...
