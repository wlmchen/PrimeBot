import yaml
from pymongo import MongoClient

__all__ = ['conf', 'db']


def load_config():
    with open("primebot/config/config.yml", "r", encoding="utf-8") as config:
        raw = yaml.safe_load(config)
    return raw


conf = load_config()
db = MongoClient(conf['mongo_db']).primebot
