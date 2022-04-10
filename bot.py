import telebot
from telebot import types
from telebot.types import LabeledPrice

API = "API_KEY"
STRIPE = "STRIPE_TEST"

provider_token = STRIPE  # @BotFather -> Bot Settings -> Payments
bot = telebot.TeleBot(API)
print("started")
prices = [LabeledPrice(label='Baby dragon', amount=100000), LabeledPrice('Time machine', 50000)]


@bot.message_handler(commands=['start'])
def start(message):
    menu = types.ReplyKeyboardMarkup()
    menu.row('Products')
    menu.row('About')
    bot.send_message(message.chat.id, 'Hello , {name} \nSelect a menu item :.'.format(name=message.chat.first_name),
                     reply_markup=menu)


@bot.message_handler(content_types=['text'])
def body(message):
    if message.text == 'Products':
        bot.send_message(message.chat.id,
                         "You will recieve an invoice now."
                         " Use this card number: <code>4242 4242 4242 4242</code>\n\n<b>Do not use your real card as funds can be lost</b>", parse_mode='HTML')
        bot.send_invoice(
            chat_id=message.chat.id,
            title='Purchase',
            description='You will make a test transaction.',
            invoice_payload='true',
            provider_token=provider_token,
            start_parameter='true',
            currency='usd',
            prices=prices
        )
    elif message.text == 'About':
        bot.send_message(message.chat.id,
                         'This is a bot made by xandee for a showcase on how telegram bots and payments work.\nThe bot is not just limited to only payments as it can do limitless things even to crypto airdrop bots')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Something went wrong"
                                                "Try again later")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'You have successfully created a transaction of ${}'.format(
                         message.successful_payment.total_amount / 100))


bot.skip_pending = True
bot.polling()
