from telebot import types
import telebot

token = 'YOUR TOKEN'
gift_lists = {}  # Словарь для хранения списков подарков пользователей
active_commands = {}  # Словарь для хранения активных команд пользователей

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, это бот, сделанный для запоминания хотелок)')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_gift = types.KeyboardButton("Добавить хотелку \U0001F48C")
    button_list_gift = types.KeyboardButton("Список хотелок \U0001F4AB")
    button_other_user = types.KeyboardButton("Просмотреть хотелки другого человека \U0001F464")
    button_cancel = types.KeyboardButton("Отменить хотелку \U0001F6AB")
    markup.add(button_gift)
    markup.add(button_list_gift)
    markup.add(button_other_user)
    markup.add(button_cancel)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    user_id = message.chat.id
    if user_id in active_commands:
        active_command = active_commands[user_id]
        if active_command == "Добавить хотелку \U0001F48C":
            add_gift(message)
        elif active_command == "Просмотреть хотелки другого человека \U0001F464":
            show_other_gifts(message)
        elif active_command == "Отменить":
            cancel_gift(message)
        del active_commands[user_id]
    else:
        if message.text == "Добавить хотелку \U0001F48C":
            bot.send_message(message.chat.id, text="Введи свою хотелку")
            active_commands[user_id] = "Добавить хотелку \U0001F48C"
        elif message.text == "Список хотелок \U0001F4AB":
            if user_id in gift_lists:
                user_gifts = gift_lists[user_id]
                if len(user_gifts) > 0:
                    for gift in user_gifts:
                        bot.send_message(message.chat.id, text=gift)
                else:
                    bot.send_message(message.chat.id, text="Список хотелок пуст!")
            else:
                bot.send_message(message.chat.id, text="Вы еще не добавили ни одной хотелки!")
        elif message.text == "Просмотреть хотелки другого человека \U0001F464":
            bot.send_message(message.chat.id, text="Введите идентификатор другого человека:")
            active_commands[user_id] = "Просмотреть хотелки другого человека \U0001F464"
        elif message.text == "Отменить хотелку \U0001F6AB":
            bot.send_message(message.chat.id, text = "Введи хотелку, которую хочешь отменить.")
            active_commands[user_id] = "Отменить"

def add_gift(message):
    user_id = message.chat.id
    gift = message.text
    if user_id in gift_lists:
        gift_lists[user_id].append(gift)
    else:
        gift_lists[user_id] = [gift]
    bot.send_message(message.chat.id, text="Хотелка добавлена!")

def show_other_gifts(message):
    other_user_id = int(message.text)
    if other_user_id in gift_lists:
        other_user_gifts = gift_lists[other_user_id]
        if len(other_user_gifts) > 0:
            for gift in other_user_gifts:
                bot.send_message(message.chat.id, text=gift)
        else:
            bot.send_message(message.chat.id, text="Список хотелок другого человека пуст!")
    else:
        bot.send_message(message.chat.id, text="У этого человека нет хотелок!")

def cancel_gift(message):
    user_id = message.chat.id
    if user_id in gift_lists:
        user_gifts = gift_lists[user_id]
        if len(user_gifts) > 0:
            last_gift = user_gifts.remove(message.text)
            bot.send_message(message.chat.id, text=f"Хотелка '{message.text}' отменена!")
        else:
            bot.send_message(message.chat.id, text="Список хотелок пуст!")
    else:
        bot.send_message(message.chat.id, text="Вы еще не добавили ни одной хотелки!")

bot.polling(none_stop=True)