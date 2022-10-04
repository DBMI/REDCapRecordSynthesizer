"""
Module: contains class NicknameGenerator, which parses "Robert" into "Bob", "Bobby" etc.

https://github.com/carltonnorthern/nickname-and-diminutive-names-lookup
"""
import collections
import csv
import os
from typing import Optional, Union
from . import get_data


# pylint: disable=too-few-public-methods
class NicknameGenerator:
    """
    Class that converts names to nicknames.

    ...

    Methods
    -------
    get(name, default=None):
        Returns the nickname for a given name. If not found, returns the specified default value.
    """

    def __init__(self, filename=None):
        """Constructs object by preloading the names.csv file.

        Parameters
        ----------
        filename : str
            Name of the .csv file containing the nicknames dictionary.

        Raises
        ------
            FileNotFoundError
                If unable to find the filename specified.
        """
        default_filename = NicknameGenerator.__names_file()
        filename = filename or default_filename
        self.__lookup = collections.defaultdict(list)

        with open(filename, encoding="utf-8") as names_csv_file:
            reader = csv.reader(names_csv_file)

            for line in reader:
                matches = set(line)

                for match in matches:
                    self.__lookup[match].append(matches)

    def get(
        self, name: str, default: Optional[str] = None
    ) -> Union[Optional[str], Optional[list]]:
        """Translates the name provided into its nicknames, if available.

        Parameters
        ----------
        name : str
            Name to translate.
        default : str
            What to return if name not found.

        Returns
        -------
        str or None
        """
        try:
            name = name.lower()
        except (AttributeError, NameError):
            return None

        if name in self.__lookup:
            names = list(set().union(*self.__lookup[name]))

            if name in names:
                names.remove(name)

            return names

        return default

    @staticmethod
    def __names_file() -> str:
        """Gets the 'names.csv' file that is expected to accompany this module.

        Returns
        -------
        default_filename : str

        Raises
        ------
            RuntimeError
                If 'names.csv' file not found in expected location.
        """
        default_filename = get_data("names.csv")

        if (
            default_filename is None
            or not isinstance(default_filename, str)
            or not os.path.exists(default_filename)
        ):
            raise RuntimeError(
                f"Unable to find file '{default_filename}'."
            )  # pragma: no cover

        return default_filename


if __name__ == "__main__":
    pass
