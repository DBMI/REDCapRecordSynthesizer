"""
Module: contains class StateAbbreviationConverter,
which converts abbreviations like 'CA' into
the full state name like 'California'.
 https://stackoverflow.com/a/66572956/18749636
"""


class StateAbbreviationConverter:  # pylint: disable=too-few-public-methods
    """
    Contains a dictionary of US state/territory names, keyed by their abbreviations.

    ...
    Attributes
    ----------
    no public attributes

    Methods
    -------
    full_name()
        Converts 'AK' to 'Alaska'.
    """

    def __init__(self):
        self.__states = {
            "AA": "Armed Forces Americas",
            "AE": "Armed Forces Europe",
            "AK": "Alaska",
            "AL": "Alabama",
            "AP": "Armed Forces Pacific",
            "AR": "Arkansas",
            "AS": "American Samoa",
            "AZ": "Arizona",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DC": "District of Columbia",
            "DE": "Delaware",
            "FL": "Florida",
            "FM": "Federated States of Micronesia",
            "GA": "Georgia",
            "GU": "Guam",
            "HI": "Hawaii",
            "IA": "Iowa",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "MA": "Massachusetts",
            "MD": "Maryland",
            "ME": "Maine",
            "MH": "Marshall Islands",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MO": "Missouri",
            "MP": "Northern Mariana Islands",
            "MS": "Mississippi",
            "MT": "Montana",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "NE": "Nebraska",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NV": "Nevada",
            "NY": "New York",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "PR": "Puerto Rico",
            "PW": "Palau",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VA": "Virginia",
            "VI": "Virgin Islands",
            "VT": "Vermont",
            "WA": "Washington",
            "WI": "Wisconsin",
            "WV": "West Virginia",
            "WY": "Wyoming",
        }

    def full_name(self, two_letter_code):
        """Converts two-letter abbreviation to a full state name.

        Parameters
        ----------
        two_letter_code string

        Returns
        -------
        string

        """
        if two_letter_code in self.__states:
            return self.__states[two_letter_code]

        return two_letter_code


if __name__ == "__main__":
    pass
