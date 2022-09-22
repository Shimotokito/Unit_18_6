import telebot
import config as conf
import extensions as ext


bot = telebot.TeleBot(conf.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Для того чтобы начать работать, введите команду для Бота в следующем формате:\n<название валюты> \
    <в какую хотите перевести> \
    <количество переводимой валюты>\nПосмотреть список доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступыне валюты:"
    for key in conf.keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        user_values = message.text.split(' ')

        if len(user_values) != 3:
            raise ext.APIException("Ошибка ввода. Введите 3 параметра.")
        quote, base, amount = user_values
        total_base = ext.MoneyConverter.get_price(quote, base, amount)
    except ext.APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} "{quote}" в "{base}" = {total_base} :-)'
        bot.send_message(message.chat.id, text)


bot.polling()
