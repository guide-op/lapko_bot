import yaml

# Provide language strings
lang_strings: dict[str, str] = {}
with open("src/lapko_bot/assets/lang.yml", "r", encoding="utf8") as f:
    lang_strings = yaml.safe_load(f)
