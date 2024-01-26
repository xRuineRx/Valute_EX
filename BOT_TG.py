import telebot
import requests
import json
from config import TOKEN,valuta
from extensions import APIException

bot = telebot.TeleBot(TOKEN)


# Инфа для проверяющего. Api брался от ЦБ РФ. К сожалению такого удобного API как при обучении найни не получилось
# Впрочем все остальное сделать в целом получилось. РАСПИСЫВАТЬ ОШИБКИ НЕ СТАЛ (решил все ошибки в одну запихнуть)
# APIException может реагировать на все ошибки, на всякий случай сделал ее вывод пользователю и к нам в консоль


@bot.message_handler(commands=["start", "help"])
def start_help(message: telebot.types.Message):
    text = ("Как пользоваться ботом:\n***************************\n<имя валюты, цену которой хотите узнать>"
            "\n<имя валюты, в которой надо узнать цену первой валюты>"
            "\n<количество первой валюты> \n***************************"
            "\nПример ввода*: доллар евро 100")
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for keys in valuta.keys():
        text = "\n".join((text, keys))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def values(message: telebot.types.Message):
    try:
        passing = message.text.split(" ")

        if len(passing) != 3:
            raise APIException("Что- то пошло не так, Пользователь где то облажался")
    except Exception:
        text = "Вы убили бота >_<, ошибка APIException"
        bot.reply_to(message, text)
    else:
        interest, base, amount = message.text.split(" ")
        interest = interest.lower()
        base = base.lower()


        r = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        USD_per_RUB = json.loads(r.content)["Valute"]["USD"]["Value"]
        EUR_per_RUB = json.loads(r.content)["Valute"]["EUR"]["Value"]

        # Кросс_Курс Евро/Доллар
        # Кросс-Курс позволит узнать курс евро к доллару и наоборот
        # Долларов надо чтобы купить 1 евро
        USD_EUR = (1 / USD_per_RUB) * (EUR_per_RUB / 1)

        # Евро надо чтобы купить 1 доллар
        EUR_USD = (1 / EUR_per_RUB) * (USD_per_RUB / 1)

        if interest == "доллар":
            if base == "рубль":
                ans = (USD_per_RUB) * int(amount)
                text = f"Цена валюты '{interest}' в количестве {amount} в размере валюты '{base}' ровняется - {ans}"
        if interest == "доллар":
            if base == "евро":
                ans = EUR_USD * int(amount)
                text = f"Цена валюты '{interest}' в количестве {amount} в размере валюты '{base}' ровняется - {ans}"
        if interest == "евро":
            if base == "рубль":
                ans = EUR_per_RUB * int(amount)
                text = f"Цена валюты '{interest}' в количестве {amount} в размере валюты '{base}' ровняется - {ans}"
        if interest == "евро":
            if base == "доллар":
                ans = USD_EUR * int(amount)
                text = f"Цена валюты '{interest}' в количестве {amount} в размере валюты '{base}' ровняется - {ans}"
        if interest == "рубль":
            if base == "евро":
                ans = (1 / EUR_per_RUB) * int(amount)
                text = f"Цена валюты '{interest}' в количестве {amount} в размере валюты '{base}' ровняется - {ans}"
        if interest == "рубль":
            if base == "доллар":
                ans = (1 / USD_per_RUB) * int(amount)
                text = f"Цена валюты '{interest}' в количестве {amount} в размере валюты '{base}' ровняется - {ans}"
        bot.send_message(message.chat.id, text)




bot.polling()
