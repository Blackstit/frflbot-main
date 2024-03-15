import telebot
from telebot import types

# Клавиатура для проверки подписки
subscribe_keyboard = telebot.types.InlineKeyboardMarkup()
btn_subscribe = telebot.types.InlineKeyboardButton(text="Подписаться", url="https://t.me/fireflycomm")
btn_check_subscribe = telebot.types.InlineKeyboardButton(text="Проверить", callback_data="check")
subscribe_keyboard.add(btn_subscribe)
subscribe_keyboard.add(btn_check_subscribe)

# Клавиатура для профиля
main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_profile = telebot.types.KeyboardButton("Профиль 👤")
btn_abot_us = telebot.types.KeyboardButton("О нас 🌐")  
main_keyboard.row(btn_profile, btn_abot_us)

# Создание инлайн кнопок
about_us_keyboard = types.InlineKeyboardMarkup()
btn_agava_crypto = types.InlineKeyboardButton("FireFly Crypto", url="https://t.me/fireflycomm")
btn_agava_crypto_chat = types.InlineKeyboardButton("FireFly Crypto Chat", url="https://t.me/+TIBhBif_kQYxZjM0")
about_us_keyboard.row(btn_agava_crypto)
about_us_keyboard.row(btn_agava_crypto_chat)

# Создаем клавиатуру для заданий
profile_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn_stats = types.InlineKeyboardButton("Статистика 📌", callback_data="profile_stats")
btn_tasks = types.InlineKeyboardButton("Задания 🎯 ", callback_data="profile_tasks")
btn_improvements = types.InlineKeyboardButton("Улучшения 🛡️", callback_data="improvements")
btn_ref_program = types.InlineKeyboardButton("Реферральная программа ⭐", callback_data="ref_program")
profile_keyboard.row(btn_stats)
profile_keyboard.row(btn_tasks, btn_improvements)
profile_keyboard.row(btn_ref_program)

#  Создаем клавиатуру для реферральной программы
def generate_ref_keyboard(reply_text_friend):
    ref_keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_send = types.InlineKeyboardButton("Отправить другу ✉️", switch_inline_query=reply_text_friend)
    btn_friend = types.InlineKeyboardButton("Мои друзья 👥", callback_data="my_ref_friends")
    btn_close = types.InlineKeyboardButton("Закрыть ❌", callback_data="close")
    ref_keyboard.add(btn_send, btn_friend, btn_close)
    return ref_keyboard

close_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn_close = types.InlineKeyboardButton("Закрыть ❌", callback_data="close")
close_keyboard.add(btn_close)