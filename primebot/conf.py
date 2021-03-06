import yaml

__all__ = ("conf")


def load_config():
    with open("primebot/config/config.yml", "r", encoding="utf-8") as config:
        raw = yaml.safe_load(config)
    return raw

conf = load_config()

