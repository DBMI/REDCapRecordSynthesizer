"""
REDCap Record Synthesizer

Class FakeRecordGenerator, which lets us synthesize
patient records with realistic data.
"""
import nickname_lookup  # type: ignore[import]  # noqa:F401

from redcap_record_synthesizer.fake_records import (  # noqa:F401
    FakeRecordGenerator,
)
from redcap_record_synthesizer.state_abbr_conversion import (  # noqa:F401
    StateAbbreviationConverter,
)
