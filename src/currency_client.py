import time
import requests
import logging.config
from config import Config
from src.decorators import cache

logging.config.fileConfig(fname='./logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class CurrencyClient(Config):
    def __init__(self, minutes):
        self.minutes = minutes

    def __get_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"

    def __get_params(self, currency_code):
        return dict(
            symbols=currency_code,
            access_key=self.access_key
        )

    def __logging(self, val, endpoint):
        if val.status_code == 200:
            logger.info(f"{self.base_url}/{endpoint} - GET - {val.status_code} ... {val.json().get('rates')}")
        else:
            logger.error(f"{self.base_url}/{endpoint} - GET - {val.status_code}")

    @cache(ttl=3)
    def get_currency(self, currency_code):
        endpoint = "latest"
        url = self.__get_url(endpoint=endpoint)
        r = requests.get(url, params=self.__get_params(currency_code=currency_code))

        self.__logging(val=r, endpoint=endpoint)
        return r.json()

    @cache(ttl=3)
    def get_historical_currency(self, currency_code, date_stamp):
        endpoint = date_stamp
        url = self.__get_url(endpoint=endpoint)
        r = requests.get(url, params=self.__get_params(currency_code=currency_code))

        self.__logging(val=r, endpoint=endpoint)
        return r.json()

    @staticmethod
    def set_interval(seconds):
        return time.sleep(seconds)
