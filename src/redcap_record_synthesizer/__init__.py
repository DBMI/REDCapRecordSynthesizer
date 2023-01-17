"""
REDCap Record Synthesizer

Class FakeRecordGenerator, which lets us synthesize
patient records with realistic data.
"""
import nickname_lookup  # type: ignore[import]  # noqa:F401
from fake_records import FakeRecordGenerator  # type: ignore[import]  # noqa:F401
from state_abbr_conversion import (  # type: ignore[import]  # noqa:F401
    StateAbbreviationConverter,
)
