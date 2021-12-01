import pytest
from jsonschema import validate
from src.currency_client import CurrencyClient
from schemas.currency_schema import CurrencySchema


def test_can_get_usd_currency():
    """ Can get USD currency from currency online server """
    client = CurrencyClient(minutes=3)
    result = client.get_currency("USD")
    assert result.get("success") is True
    validate(instance=result, schema=CurrencySchema.success_schema())


def test_cannot_get_currency_for_invalid_currency_code():
    """ Cannot get currency from currency online server with an invalid currency code"""
    client = CurrencyClient(minutes=3)
    result = client.get_currency("USX")
    assert result["error"].get("code") == "invalid_currency_codes"
    assert result["error"].get("message") == "You have provided one or more invalid Currency Codes. " \
                                             "[Required format: currencies=EUR,USD,GBP,...]"
    validate(instance=result, schema=CurrencySchema.invalid_currency_code_schema())


def test_can_get_multiple_currencies():
    """ Can get Multiple currencies from currency online server """
    client = CurrencyClient(minutes=3)
    result = client.get_currency("USD,ZAR,AUD,PLN")
    assert result.get("success") is True
    assert "USD" in result.get("rates")
    assert "ZAR" in result.get("rates")
    assert "AUD" in result.get("rates")
    assert "PLN" in result.get("rates")
    validate(instance=result, schema=CurrencySchema.success_schema())


def test_can_get_currency_from_cache():
    """ Can get USD currency from cache """
    client = CurrencyClient(minutes=3)
    client.get_currency("USD")
    cached_result = client.get_currency("USD")
    assert cached_result.get("cached") is True


def test_can_get_currency_from_server_after_ttl_expires():
    """ Can get multiple currencies from currency online server after ttl expired """
    client = CurrencyClient(minutes=3)
    client.get_currency("USD,ZAR,AUD,PLN")
    cached_result = client.get_currency("USD,ZAR,AUD,PLN")
    assert cached_result.get("cached") is True
    client.set_interval(seconds=4)
    result = client.get_currency("USD,ZAR,AUD,PLN")
    assert result.get("cached") is None
