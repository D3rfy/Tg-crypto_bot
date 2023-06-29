# 6309898306:AAGvVJ3QTc5JgsqFBycXkTE6mdyKfYtIfJk | token
# pip install pyTelegramBotAPI
# pip install -U pycoingecko
# pip install py-currency-converter

import telebot
from telebot import types
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

bot = telebot.TeleBot('6309898306:AAGvVJ3QTc5JgsqFBycXkTE6mdyKfYtIfJk')

@bot.message_handler(commands=['crypto'])
def main(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Получить курс криптовалют'))
    cr = bot.send_message(message.chat.id, 'Мы на главной', reply_markup=b1)
    bot.register_next_step_handler(cr, step2)

def step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Перейти'))

    price = cg.get_price(ids='bitcoin, ethereum, litecoin, solana, uniswap', vs_currencies='usd')
    bot.send_message(message.chat.id, f'Мои токены:\n\n'
                     f'Bitcoin == {price["bitcoin"]["usd"]} $\n'
                     f'Ethereum == {price["ethereum"]["usd"]} $\n'
                     f'Litecoin == {price["litecoin"]["usd"]} $\n'
                     f'Solana == {price["solana"]["usd"]} $\n'
                     f'Uniswap == {price["uniswap"]["usd"]} $\n', reply_markup=b1)
    go_main = bot.send_message(message.chat.id, 'Перейти на главную?', reply_markup=b1)
    bot.register_next_step_handler(go_main, main)

bot.polling()