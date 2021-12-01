import os


class Config(object):
    base_url = "http://api.exchangeratesapi.io/v1"
    access_key = os.getenv("ACCESS_KEY")
