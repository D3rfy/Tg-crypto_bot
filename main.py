# 6309898306:AAGvVJ3QTc5JgsqFBycXkTE6mdyKfYtIfJk | token
# pip install pyTelegramBotAPI
# pip install -U pycoingecko
# pip install py-currency-converter

import telebot
from telebot import types
from pycoingecko import CoinGeckoAPI
from py_currency_converter import convert
cg = CoinGeckoAPI()

bot = telebot.TeleBot('6309898306:AAGvVJ3QTc5JgsqFBycXkTE6mdyKfYtIfJk')

@bot.message_handler(commands=['start'])
def main(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Получить курс криптовалют'), types.KeyboardButton('Получить курс валют'))
    cr = bot.send_message(message.chat.id, 'Мы на главной', reply_markup=b1)
    bot.register_next_step_handler(cr, step)

def step(message):
    if message.text == 'Получить курс криптовалют':
        step2(message)

    elif message.text == 'Получить курс валют':
        fiat(message)

def fiat(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('USD'), types.KeyboardButton('RUB'), types.KeyboardButton('Главная'))
    q = bot.send_message(message.chat.id, 'Курс валют', reply_markup=b1)
    bot.register_next_step_handler(q, fiat_step2)

def fiat_step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Назад'))

    if message.text == 'USD':
        price = convert(base='USD', amount=1, to=['RUB', 'EUR', 'CNY', 'KZT'])
        bot.send_message(message.chat.id, f'1 USD == {price["RUB"]} RUB\n'
                                          f'1 USD == {price["EUR"]} EUR\n'
                         f'1 USD == {price["CNY"]} CNY\n'
                         f'1 USD == {price["KZT"]} KZT')
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, fiat)

    elif message.text == 'RUB':
        price = convert(base='RUB', amount=1, to=['USD', 'EUR', 'CNY', 'KZT'])
        bot.send_message(message.chat.id, f'1 RUB == {price["USD"]} USD\n'
                                          f'1 RUB == {price["EUR"]} EUR\n'
                         f'1 RUB == {price["CNY"]} CNY\n'
                         f'1 RUB == {price["KZT"]} KZT')
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, fiat)

    if message.text == 'Главная':
        main(message)

def step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Курс к USD'), types.KeyboardButton('Курс к RUB'), types.KeyboardButton('Главная'))
    q = bot.send_message(message.chat.id, 'Курс моих токенов', reply_markup=b1)
    bot.register_next_step_handler(q, step3)

def step3(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Назад'))

    if message.text == 'Курс к USD':
        price = cg.get_price(ids='bitcoin, ethereum, litecoin, solana, uniswap', vs_currencies='usd')
        bot.send_message(message.chat.id, f'Мои токены:\n\n'
                                          f'Bitcoin == {price["bitcoin"]["usd"]} $\n'
                                          f'Ethereum == {price["ethereum"]["usd"]} $\n'
                                          f'Litecoin == {price["litecoin"]["usd"]} $\n'
                                          f'Solana == {price["solana"]["usd"]} $\n'
                                          f'Uniswap == {price["uniswap"]["usd"]} $\n', reply_markup=b1)
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, step2)

    elif message.text == 'Курс к RUB':
        price = cg.get_price(ids='bitcoin, ethereum, litecoin, solana, uniswap', vs_currencies='rub')
        bot.send_message(message.chat.id, f'Мои токены:\n\n'
                                            f'Bitcoin == {price["bitcoin"]["rub"]} ₽\n'
                                            f'Ethereum == {price["ethereum"]["rub"]} ₽\n'
                                            f'Litecoin == {price["litecoin"]["rub"]} ₽\n'
                                            f'Solana == {price["solana"]["rub"]} ₽\n'
                                            f'Uniswap == {price["uniswap"]["rub"]} ₽\n', reply_markup=b1)
        go_main = bot.send_message(message.chat.id, 'Вернуться назад?', reply_markup=b1)
        bot.register_next_step_handler(go_main, step2)

    elif message.text == 'Главная':
        main(message)
bot.polling()