class APIException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{type(self).__name__}: {self.message}"

import requests
import json

class CryptoCompareAPI:
    @staticmethod
    def get_price(base, quote, amount):
        url = f"https://min-api.cryptocompare.com/data/price?fsym={base.upper()}&tsyms={quote.upper()}"
        response = requests.get(url)
        if response.status_code != 200:
            raise APIException("API unavailable")

        data = json.loads(response.text)
        if quote.upper() not in data:
            raise APIException("Invalid quote currency")

        if not isinstance(amount, (int, float)):
            raise APIException("Invalid amount value")

        return data[quote.upper()] * amount

import telebot

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commands=['start', 'help'])
        def send_instructions(message):
            instructions = "ПРИВЕТ Я помогу тебе узнать актуальный курс валют! Введите сообщение в формате: <имя валюты цену которой вы хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты> НАПРИМЕР: USD RUB 1 <ОТВЕТ БУДЕТ <1 USD = ..RUB> Узнать доступные валюты /values "
            self.bot.send_message(message.chat.id, instructions)

        @self.bot.message_handler(commands=['values'])
        def send_values(message):
            values = "Доступные валюты: USD, EUR, RUB"
            self.bot.send_message(message.chat.id, values)

        @self.bot.message_handler(func=lambda message: True)
        def send_price(message):
            try:
                base, quote, amount = message.text.split()
                price = CryptoCompareAPI.get_price(base, quote, float(amount))
                response = f"{amount} {base.upper()} = {price} {quote.upper()}"
            except ValueError:
                response = "Неверный формат запроса. Введите сообщение в формате: <имя валюты цену которой вы хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты> НАПРИМЕР: USD RUB 1 Узнать доступные валюты /values"
            except APIException as e:
                response = str(e)

            self.bot.send_message(message.chat.id, response)

        @self.bot.message_handler(func=lambda message: True)
        def send_price(message):
            try:
                base, quote, amount = message.text.split()
                price = CryptoCompareAPI.get_price(base, quote, float(amount))
                response = f"{amount} {base.upper()} = {price} {quote.upper()}"
            except APIException as e:
                response = str(e)

            self.bot.send_message(message.chat.id, response)

    def start(self):
        self.bot.polling(none_stop=True)
