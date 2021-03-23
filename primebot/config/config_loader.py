import yaml
from pymongo import MongoClient
from primebot.utils import gazelle

__all__ = ['conf', 'db', 'sows']


def load_config():
    with open("primebot/config/config.yml", "r", encoding="utf-8") as config:
        raw = yaml.safe_load(config)
    return raw


conf = load_config()
db = MongoClient(conf['mongo_db']).primebot
sows = gazelle.WhatAPI(conf['sows']['username'], conf['sows']['password'])
