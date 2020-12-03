import telebot
from config import keys, TOKEN
from utils import ConvertException, CryptoConvertor
 
bot = telebot.TeleBot(TOKEN)





# write simple answer to our every message
# def echo_test(message: telebot.types.Message):
#    bot.send_message(message.chat.id, 'hello')

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> <в какую валюту перевести> \n<количество переводимой валюты>\n<увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def  get_price(message: telebot.types.Message):
    # биткоин доллар 1
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConvertException('Слищком много параметров.')

        quote, base, amount = values
        total_base = CryptoConvertor.convert(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)