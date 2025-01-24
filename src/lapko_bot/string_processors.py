from operator import itemgetter

import regex as re

from src.lapko_bot.helpers.enums import QuoteWarnings


def quotify(text: str) -> str:
    # Sub quote sequences at word and punctuation boundaries
    text = re.sub(r'["“»”]+(?=[\w])', lambda t: "«" * len(t.group(0)), text)
    text = re.sub(r'(?<=[\w?!.])["“«”]+', lambda t: "»" * len(t.group(0)), text)

    # Sub nested quotes
    quote_nesting_level = 0
    text_by_char = list(text)
    for i in range(len(text)):
        if text[i] == "«":
            quote_nesting_level += 1
            if quote_nesting_level > 1:
                text_by_char[i] = "“"
        elif text[i] == "»":
            if quote_nesting_level > 1:
                text_by_char[i] = "”"
            quote_nesting_level -= 1

    return "".join(text_by_char)


def validate_quotes(text: str) -> bool:
    stack = []
    warnings = []
    for i, char in enumerate(text):
        if char not in "«»“”":
            continue
        if char == "«" or char == "“":
            stack.append((char, i))
        else:
            if char == "»":
                if not stack:
                    warnings.append((QuoteWarnings.QUOTE_UNOPENED, i))
                    continue
                if stack[-1][0] == "“":
                    warnings.append((QuoteWarnings.QUOTE_MISMATCH, i))
                stack.pop()
            elif char == "”":
                if not stack:
                    warnings.append((QuoteWarnings.QUOTE_UNOPENED, i))
                    continue
                if stack[-1][0] == "«":
                    warnings.append((QuoteWarnings.QUOTE_MISMATCH, i))
                stack.pop()
    while stack:
        if stack[-1][0] == "“":
            warnings.append((QuoteWarnings.QUOTE_UNCLOSED, stack[-1][1]))
        elif stack[-1][0] == "«":
            warnings.append((QuoteWarnings.QUOTE_UNCLOSED, stack[-1][1]))
        stack.pop()

    floating_quotes = re.finditer(r'(?<=\s)[«»“”"](?=\s)', text)
    for match in floating_quotes:
        warnings.append((QuoteWarnings.QUOTE_FLOATING, match.start()))
    return sorted(warnings, key=itemgetter(1))


def apostrify(text: str) -> str:
    # Sub apostrophes at word boundaries
    text = re.sub(r"(?<=\w)'(?=\w)", "’", text)
    return text


def dashify(text: str) -> str:
    # Convert double/triple-hyphens into en/em dashes
    text = re.sub(r"---", "—", text)
    text = re.sub(r"--", "–", text)

    # Convert double-attached em dashes appended to at least one number to en dashes
    text = re.sub(r"(?<=\w)—(?=\d)|(?<=\d)—(?=\w)", r"–", text)

    # Convert hyphens and em dashes neighbored by two numbers to en dashes
    # Compress spaces around en dashes in the process (vanilla lookbehind
    #   assertions don't support variable-length patterns, and there's no
    #   good reason to force regex ?V1 lookbehinds)
    # Do the same for roman numerals
    text = re.sub(r"(?<=\d)\s*(-|–|—)\s*(?=\d)", r"–", text)
    text = re.sub(r"(?<=[IVXLCDM])\s*(-|–|—)\s*(?=[IVXLCDM])", r"–", text)

    # Detach hyphens and dashes that are attached to words from one side
    # text = re.sub(r"(?<=\w)(-|–|—)(?=\W|$)", r" \1", text)
    # text = re.sub(r"(?<=^|\W)(-|–|—)(?=\w)", r"\1 ", text)
    text = re.sub(r"(?<=\S)(-|–|—)(?=\s|$)", r" \1", text)
    text = re.sub(r"(?<=^|\s)(-|–|—)(?=\S)", r"\1 ", text)

    # Detach em dashes that are attached to words from both sides
    # Also detach en dashes that are attached to word-letters
    #   (not digits or roman numerals) from both sides
    text = re.sub(r"(?<=\S)(—)(?=\S)", r" \1 ", text)
    text = re.sub(r"(?V1)(?<=[\p{L}--IVXLCDM])(–)(?=[\p{L}--IVXLCDM])", r" \1 ", text)

    # Convert free-floating hyphens and en dashes into em dashes
    text = re.sub(r"^(-|–)|(?<=\W)(-|–)(?=\W)", "—", text)

    return text


def compress_spaces(text: str) -> str:
    # Compress repeated spaces
    text = re.sub(r" +", " ", text)

    # Compress spaces around punctuation
    text = re.sub(r" +(?=[,.:;!?])", "", text)

    # Compress leading/trailing spaces around right/left quotes
    text = re.sub(r" +(?=[»”])", "", text)
    text = re.sub(r"(?<=[«“]) +", "", text)

    return text


def fix(text: str) -> str:
    text = quotify(text)
    text = apostrify(text)
    text = dashify(text)
    text = compress_spaces(text)
    warnings = validate_quotes(text)
    return text, warnings
