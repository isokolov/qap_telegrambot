import requests
import json

ruble_json = requests.get(f'https://api.exchangeratesapi.io/latest?symbols=RUB')
total_base = json.loads(ruble_json.content)['rates']['RUB']
print(total_base)