from enum import Enum, auto


class QuoteWarnings(Enum):
    QUOTE_UNOPENED = auto()
    QUOTE_UNCLOSED = auto()
    QUOTE_FLOATING = auto()
    QUOTE_MISMATCH = auto()


class BotResponseMessageTypes(Enum):
    START = auto()
    HELP = auto()
    SETTINGS = auto()
    UNKNOWN_CMD = auto()
    REPLY_WITH_FIX = auto()
    REPLY_WITH_WARNINGS = auto()
