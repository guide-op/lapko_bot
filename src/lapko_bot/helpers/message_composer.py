from typing import List, Tuple
from src.lapko_bot.assets import lang_strings
from src.lapko_bot.helpers.enums import BotResponseMessageTypes, QuoteWarnings

CONTEXT_RADIUS = 10


def _format_quote_warnings(quote_warnings: List[Tuple[QuoteWarnings, int]], text: str):
    formatted_warnings = [lang_strings["warnings_message_header"]]
    for quote_warning in quote_warnings:
        warning_type, warning_location = quote_warning
        warning_text = lang_strings[warning_type.name].format(
            text[warning_location],
            (
                text[max(0, warning_location - CONTEXT_RADIUS) : warning_location]
                + f">>>{text[warning_location]}<<<"
                + text[
                    warning_location
                    + 1 : min(len(text), warning_location + CONTEXT_RADIUS + 1)
                ]
            ),
        )
        formatted_warnings.append(warning_text)
    return "\n".join(formatted_warnings)


_response_selector = {
    BotResponseMessageTypes.START: lambda: lang_strings["on_cmd_start"],
    BotResponseMessageTypes.HELP: lambda: lang_strings["on_cmd_help"],
    BotResponseMessageTypes.SETTINGS: lambda: lang_strings["on_cmd_settings"],
    BotResponseMessageTypes.UNKNOWN_CMD: lambda: lang_strings["on_cmd_<unknown>"],
    BotResponseMessageTypes.REPLY_WITH_FIX: lambda text: text,
    BotResponseMessageTypes.REPLY_WITH_WARNINGS: _format_quote_warnings,
}


def compose_message(message_type: BotResponseMessageTypes, **kwargs) -> str:
    return _response_selector[message_type](**kwargs)
