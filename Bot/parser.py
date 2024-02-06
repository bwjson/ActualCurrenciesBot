import requests

class Parser:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stock_price(self, symbol):
        url = f'https://api.finage.co.uk/last/stock/{symbol}?apikey={self.api_key}'
        response = requests.get(url)
        data = response.json()
        if 'ask' in data:
            return data['ask']
        else:
            return "Unable to fetch data"

    def get_convert(self, from_curr, to_curr, amount):
        url = f'https://api.finage.co.uk/convert/forex/{from_curr}/{to_curr}/{amount}?apikey={self.api_key}'
        response = requests.get(url)
        data = response.json()
        if 'value' in data:
            return data['value']
        else:
            return 'Unable to fetch data'

    def get_news(self, symbol):
        url = f'https://api.finage.co.uk/news/market/{symbol}?apikey={self.api_key}'
        response = requests.get(url)
        data = response.json()
        if 'news' in data and 'news' != '':
            news_data = '\n'.join([f"{article['title']} - {article['url']}" for article in data['news']])
            return news_data
        else:
            return 'Unable to fetch data'






