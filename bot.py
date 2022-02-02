import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption

API = "1854723686:AAFTyVNy4TlCJWzQVQ_avT0jA9RDPscFGrg"
STRIPE = "284685063:TEST:YWYyZWU2ZDc3ZmIw"

provider_token = STRIPE  # @BotFather -> Bot Settings -> Payments
bot = telebot.TeleBot(API)

prices = [LabeledPrice(label='Цена', amount=10000), LabeledPrice('Комиссия', 0)]


@bot.message_handler(commands=['start'])
def start(message):
    menu = types.ReplyKeyboardMarkup()
    menu.row('Products')
    menu.row('About the bot')
    bot.send_message(message.chat.id, 'Hello , {name} \nSelect a menu item :.'.format(name=message.chat.first_name),
                     reply_markup=menu)


@bot.message_handler(content_types=['text'])
def body(message):
    if message.text == 'Products':
        bot.send_message(message.chat.id,
                         "You will recieve an invoice now."
                         " Use this card number: `4242 4242 4242 4242`", parse_mode='Markdown')
        bot.send_invoice(
            chat_id=message.chat.id,
            title='Тест',
            description='You will make a test transaction.',
            invoice_payload='true',
            provider_token=provider_token,
            start_parameter='true',
            currency='rub',
            prices=prices
        )
    elif message.text == 'About the bot':
        bot.send_message(message.chat.id,
                         'This is a bot store with Yandex cashier.\nWant to yourself the same?\nCan you order it from us @LifeCode_Bot')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Something went wrong"
                                                "Try again later")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'You have successfully created a transaction on `{} {}`! '.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


bot.skip_pending = True
bot.polling()
