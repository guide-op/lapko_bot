import re


def quotify(text: str) -> str:
    # Sub quote sequences at word and punctuation boundaries
    text = re.sub(r'["“]+(?=[\w])', lambda t: "«" * len(t.group(0)), text)
    text = re.sub(r'(?<=[\w?!.])["”]+', lambda t: "»" * len(t.group(0)), text)

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


def emdashify(text: str) -> str:
    # Separate hyphens and en dashes that are glued to words from one side
    text = re.sub(r"(?<=\w)(--?-?|–|—)(?=\W)", r" \1", text)
    text = re.sub(r"(?<=\W)(--?-?|–|—)(?=\w)", r"\1 ", text)
    text = re.sub(r"^(--?-?|–|—)(?=\w)", r"\1 ", text)

    # Convert free-floating hyphens and en dashes
    text = re.sub(r"(?<=\W)(--?-?|–)(?=\W)", "—", text)
    text = re.sub(r"^(--?-?|–)", "—", text)

    return text


def compress_spaces(text: str) -> str:
    # Compress repeated spaces
    text = re.sub(r" +", " ", text)

    # Compress spaces around punctuation
    text = re.sub(r" (?=[,.:;!?])", "", text)

    return text


def fix(text: str) -> str:
    text = quotify(text)
    text = emdashify(text)
    text = compress_spaces(text)
    return text
