import yaml
from pymongo import MongoClient
from primebot.utils import gazelle

__all__ = ['conf', 'db', 'sows', 'ops']


def load_config():
    with open("primebot/config/config.yml", "r", encoding="utf-8") as config:
        raw = yaml.safe_load(config)
    return raw


conf = load_config()
db = MongoClient(conf['mongo_db']).primebot
sows = sows.WhatAPI(conf['sows']['username'], conf['sows']['password'])

conf = load_config()
db = MongoClient(conf['mongo_db']).primebot
ops = ops.WhatAPI(conf['ops']['username'], conf['ops']['password'])
