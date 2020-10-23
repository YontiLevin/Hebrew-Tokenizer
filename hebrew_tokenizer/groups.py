
class Groups:
    WHITESPACE = "WHITESPACE"
    DATE_1 = "DATE_1"
    DATE_2 = "DATE_2"
    DATE = "DATE"
    HOUR = "HOUR"
    NUMBER = "NUMBER"
    URL = "URL"
    PUNCTUATION = "PUNCTUATION"
    ENGLISH_1 = "ENGLISH_1"
    ENGLISH_2 = "ENGLISH_2"
    ENGLISH = "ENGLISH"
    HEBREW_1 = "HEBREW_1"
    HEBREW_2 = "HEBREW_2"
    HEBREW = "HEBREW"
    OTHER = "OTHER"
    LINEBREAK = "LINEBREAK"
    BOM = "BOM"
    REPEATED = "REPEATED"


GroupsReverseMapping = {
    "WHITESPACE": "WHITESPACE",
    "DATE_1": "DATE",
    "DATE_2": "DATE",
    "DATE": "DATE",
    "HOUR": "HOUR",
    "NUMBER": "NUMBER",
    "URL": "URL",
    "PUNCTUATION": "PUNCTUATION",
    "ENGLISH_1": "ENGLISH",
    "ENGLISH_2": "ENGLISH",
    "ENGLISH": "ENGLISH",
    "HEBREW_1": "HEBREW",
    "HEBREW_2": "HEBREW",
    "HEBREW": "HEBREW",
    "OTHER": "OTHER",
    "LINEBREAK": None,
    "BOM": None,
    "REPEATED": None,
}

# class Groups(Enum):
#     WHITESPACE = auto()
#     DATE = auto()
#     HOUR = auto()
#     NUMBER = auto()
#     URL = auto()
#     PUNCTUATION = auto()
#     ENGLISH = auto()
#     HEBREW = auto()
#     OTHER = auto()
