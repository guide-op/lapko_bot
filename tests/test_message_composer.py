# import pytest
from src.lapko_bot.assets import lang_strings
from src.lapko_bot.helpers.enums import BotResponseMessageTypes, QuoteWarnings
from src.lapko_bot.helpers.message_composer import compose_message, CONTEXT_RADIUS


def test_compose_message_start():
    assert (
        compose_message(BotResponseMessageTypes.START) == lang_strings["on_cmd_start"]
    )


def test_compose_message_help():
    assert compose_message(BotResponseMessageTypes.HELP) == lang_strings["on_cmd_help"]


def test_compose_message_settings():
    assert (
        compose_message(BotResponseMessageTypes.SETTINGS)
        == lang_strings["on_cmd_settings"]
    )


def test_compose_message_unknown_cmd():
    assert (
        compose_message(BotResponseMessageTypes.UNKNOWN_CMD)
        == lang_strings["on_cmd_<unknown>"]
    )


def test_compose_message_reply_with_fix():
    text = "This is a test message."
    assert compose_message(BotResponseMessageTypes.REPLY_WITH_FIX, text=text) == text


def test_compose_message_reply_with_warnings():
    text = "Unclosed « found."
    warning_location = text.find("«")
    quote_warnings = [(QuoteWarnings.QUOTE_UNOPENED, warning_location)]
    warning_message = lang_strings[QuoteWarnings.QUOTE_UNOPENED.name].format(
        text[warning_location],
        text[max(0, warning_location - CONTEXT_RADIUS) : warning_location]
        + f">>>{text[warning_location]}<<<"
        + text[
            warning_location + 1 : min(len(text), warning_location + CONTEXT_RADIUS + 1)
        ],
    )
    expected_warning_message = (
        f"{lang_strings['warnings_message_header']}" f"\n{warning_message}"
    )
    assert (
        compose_message(
            BotResponseMessageTypes.REPLY_WITH_WARNINGS,
            quote_warnings=quote_warnings,
            text=text,
        )
        == expected_warning_message
    )
