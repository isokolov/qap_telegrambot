import requests
import json
from config import keys


class ConvertException(Exception):
    pass 

class CryptoConvertor:
    
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        
        if quote == base:
            raise ConvertException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не удалось обработать количество {amount}.')
        ruble_json = requests.get(f'https://api.exchangeratesapi.io/latest?symbols=RUB')
        #print(ruble_json)
        dollar_json = requests.get(f'https://api.exchangeratesapi.io/latest?symbols=USD')
        ruble_rate = float(json.loads(ruble_json.content)['rates']['RUB'])
        dollar_rate = float(json.loads(dollar_json.content)['rates']['USD'])
        if base_ticker == "EUR":
            if quote_ticker == "RUB":
                return round((1 / ruble_rate) * float(amount), 1)
            if quote_ticker == "USD":
                return round((1 / dollar_rate) * float(amount), 1)
        if base_ticker == "USD":
            if quote_ticker == "EUR":
                return round(dollar_rate * float(amount), 2)
            if quote_ticker == "RUB":
                return round(((dollar_rate/ruble_rate) * float(amount)), 2)
        
        if base_ticker == "RUB":
            if quote_ticker == "EUR":
                return round(ruble_rate * float(amount), 2)
            if quote_ticker == "USD":
                return round(((ruble_rate/dollar_rate) * float(amount)), 2)
        
        
