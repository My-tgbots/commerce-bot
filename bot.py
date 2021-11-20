# -*- coding: utf-8 -*-
import os
import telebot

token = os.environ['TELEGRAM_TOKEN']

from telebot import types
from json import load, dump
from time import time
from math import floor

bot = telebot.TeleBot(token)

# Paste from here to github
data = {}

def back_main():
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Back", callback_data="back")
    keyboard.add(callback_button)
    return keyboard

def write_in_file(d, file_name="data.json"):
    with open(file_name, "w") as f:
        dump(d, f, indent=2)


def load_file(file_name="data.json"):
    try:
        with open(file_name) as json_file:
            d = load(json_file)
            return d
    except FileNotFoundError:
        write_in_file({})
        return {}

@bot.message_handler(content_types=["text"])
@bot.message_handler(commands=['help', 'start'])
def help_start(msg):
    keyboard = types.InlineKeyboardMarkup()
    mine = types.InlineKeyboardButton(text='Click to mine', callback_data='mine')
    about = types.InlineKeyboardButton(text="About", callback_data='about')
    keyboard.add(mine)
    keyboard.add(about)
    text = "Hello " + msg.chat.first_name + "\nWelcome to <b>Davies BTC miner</b>\nEarn free btc by mining with just one click ...... \n blah blah blah.......\n Just click mine"
    try:
        bot.edit_message_text(text, msg.chat.id, message_id=msg.message_id, parse_mode="HTML", reply_markup=keyboard)
    except:
        bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def answer_query(call):
    if call.message:
        if call.data == 'back':
            help_start(call.message)
        elif call.data == 'mine':
            data = load_file()
            if not str(call.message.chat.id) in data:
                data[str(call.message.chat.id)] = {"time":time()}
                write_in_file(data)
            user = data[str(call.message.chat.id)]
            kb = types.InlineKeyboardMarkup()
            withdraw = types.InlineKeyboardButton(text='Withdraw', callback_data="withdraw")
            back_btn = types.InlineKeyboardButton(text="Back", callback_data="back")
            kb.add(withdraw)
            kb.add(back_btn)
            txt = f"Current rate: 10H/s\nEarnings per day 0.86 btc\n\nCurrent amount mined: {str((floor(time()) - user['time'])*0.00001)}\n\nRefer friends to earn more: t.me/xandee_btc_miner"
            bot.edit_message_text(txt, call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML",
                                  reply_markup=kb)
        elif call.data == "about":
            bot.edit_message_text("This is to show u mf's that all these shit are scam and you should stop coming to my f***ing dm with all these f***ing links", 
            call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML",
                                  reply_markup=back_main())
        elif call.data == "withdraw":
            bot.send_message(1289366093, call.message.chat.first_name+" tried to withdraw lol")
            kb = types.InlineKeyboardMarkup()
            back_btn = types.InlineKeyboardButton(text="Back", callback_data="back")
            kb.add(back_btn)
            txt = "To withdraw:\nYou must have 100000 btc\nYou must send 0.01 btc to <i>kgjsrnhrbfherdfhebdfhfdljk</i> address to confirm your wallet (If you try it your money don jakpa)\nYou must Refer 1000 friends\nBlah blah blah .........."
            bot.edit_message_text(txt, call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML",
                                  reply_markup=kb)
bot.polling(none_stop=True)
