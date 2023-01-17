"""
REDCap Record Synthesizer

Class FakeRecordGenerator, which lets us synthesize
patient records with realistic data.
"""
from fake_records import FakeRecordGenerator
import nickname_lookup  # type: ignore[import]  # noqa:F401
from state_abbr_conversion import StateAbbreviationConverter
