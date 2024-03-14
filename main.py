import telebot
from telebot import types
import pymongo
import os
from datetime import datetime
import random
import string
import media
import time

# Загрузка переменных окружения из файла .env
from dotenv import load_dotenv
load_dotenv()

# Подключение к MongoDB
MONGO_URL = os.getenv("MONGO_URL")
client = pymongo.MongoClient(MONGO_URL)
db = client['test']  # Замените 'your_database_name' на имя вашей базы данных
users_collection = db['users']
tasks_collection = db['completed_tasks']
users_stats_collection = db['users_stats']

# Ваш бот
token = os.getenv('TELEGRAM_BOT_TOKEN_MAIN')
bot = telebot.TeleBot(token)

# ID вашего канала
chan_id = -1002109241014

# Клавиатура для проверки подписки
клавиатура_inline = telebot.types.InlineKeyboardMarkup()
подписаться = telebot.types.InlineKeyboardButton(text="Подписаться", url="https://t.me/fireflycomm")
вступить_в_чат = telebot.types.InlineKeyboardButton(text="Вступить в чат", url="https://t.me/+TIBhBif_kQYxZjM0")
проверить = telebot.types.InlineKeyboardButton(text="Проверить", callback_data="check")
клавиатура_inline.add(подписаться)
клавиатура_inline.add(вступить_в_чат)
клавиатура_inline.add(проверить)

# Клавиатура для профиля
клавиатура_профиля = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
кнопка_профиль = telebot.types.KeyboardButton("Профиль 👤")
кнопка_о_нас = telebot.types.KeyboardButton("О нас 🌐")  
клавиатура_профиля.row(кнопка_профиль, кнопка_о_нас)

# Функция для генерации случайного реферрального кода
def generate_referral_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

import telebot
from telebot import types
import pymongo
import os
from datetime import datetime
import random
import string
import media
import time

# Загрузка переменных окружения из файла .env
from dotenv import load_dotenv
load_dotenv()

# Подключение к MongoDB
MONGO_URL = os.getenv("MONGO_URL")
client = pymongo.MongoClient(MONGO_URL)
db = client['test']  # Замените 'your_database_name' на имя вашей базы данных
users_collection = db['users']
tasks_collection = db['completed_tasks']
users_stats_collection = db['users_stats']

# Ваш бот
token = os.getenv('TELEGRAM_BOT_TOKEN_MAIN')
bot = telebot.TeleBot(token)

# ID вашего канала
chan_id = -1002109241014

# Клавиатура для проверки подписки
клавиатура_inline = telebot.types.InlineKeyboardMarkup()
подписаться = telebot.types.InlineKeyboardButton(text="Подписаться", url="https://t.me/fireflycomm")
вступить_в_чат = telebot.types.InlineKeyboardButton(text="Вступить в чат", url="https://t.me/+TIBhBif_kQYxZjM0")
проверить = telebot.types.InlineKeyboardButton(text="Проверить", callback_data="check")
клавиатура_inline.add(подписаться)
клавиатура_inline.add(вступить_в_чат)
клавиатура_inline.add(проверить)

# Клавиатура для профиля
клавиатура_профиля = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
кнопка_профиль = telebot.types.KeyboardButton("Профиль 👤")
кнопка_о_нас = telebot.types.KeyboardButton("О нас 🌐")  
клавиатура_профиля.row(кнопка_профиль, кнопка_о_нас)

# Функция для генерации случайного реферрального кода
def generate_referral_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Проверяем, передан ли реферальный код в команде "/start"
    referer_code = None
    parts = message.text.split()
    if len(parts) > 1:
        referer_code = parts[1]

    print(f"{username} - Реферральный код: {referer_code} мессадж: {message.text}")

    # Проверяем, зарегистрирован ли уже пользователь
    user_data = users_collection.find_one({"_id": str(user_id)})
    print(f"{username} - Старт. юзер дата: {user_data}")
    if not user_data:
        # Генерируем уникальный реферральный код
        referral_code = generate_referral_code()
        referral_link = f"t.me/FireFlyCCbot?start={referral_code}"
        print(f"{username} - Старт. реф код ген: {referral_code}")
        # Поиск пользователя с реферральным кодом
        referrer_id = None
        if referral_code:
            referrer_data = users_collection.find_one({"referral_code": referer_code})
            if referrer_data:
                referrer_id = referrer_data['_id']

        # Добавляем пользователя в базу данных
        user = {
            "_id": str(user_id),
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "is_admin": 0, # Дефолтное значение
            "is_registered": True,
            "registration_date": registration_date,
            "email": "",  # Дефолтное значение
            "referral_code": referral_code,
            "referral_link": referral_link,
            "balance": 0,  # Дефолтное значение
            "reputation": 0,
            "message_cost": 0.5,
            "improvements": {},  # Дефолтное значение
            "tasks_completed": [],  # Дефолтное значение
            "roles": [{
                "role_id": "Newbie",
                "role_name": "Glowworm Apprentice",
                "description": "Ученик Сияющего Червяка - новый участник, только начинающий свой путь в мире криптовалют и чата 'Firefly Crypto'."
            }],
            "referrer_id": referrer_id
        }
        users_collection.insert_one(user)

        # Отправляем сообщение о подписке и кнопку профиля
        bot.send_message(user_id, f"Добро пожаловать в мир FireFly Crypto!", reply_markup=клавиатура_профиля)
        bot.send_message(user_id, """Приветствуем тебя в нашем комьюнити крипто-энтузиастов!

Мы ищем активных участников, готовых вкладывать свое время и энергию в наше сообщество, чтобы вместе стремиться к успеху!

Прежде чем присоединиться к нам, подпишись на наш Telegram-канал и создай свой профиль в этом боте.

Здесь ты сможешь отслеживать свой прогресс, получать награды и поощрения от FireFly Crypto! Давай двигаться к успеху вместе!""", reply_markup=клавиатура_inline)
    else:
        # Отправляем приветственное сообщение
        bot.send_message(user_id, "С возвращением!", reply_markup=клавиатура_профиля)

        
@bot.callback_query_handler(func=lambda call: call.data == "check")
def c_listener(call):
    user_id = call.message.chat.id
    x = bot.get_chat_member(chan_id, user_id)

    if x.status in ["member", "creator", "administrator"]:
        user_data = users_collection.find_one({"id": user_id})
        print(f"Чек, юзер дата: {user_data}")
        if user_data:
            # Получаем ID реферрера
            referrer_id = user_data['referrer_id']
            if referrer_id is not None:
                # Увеличиваем счетчик рефералов
                users_collection.update_one({"id": referrer_id}, {"$inc": {"referrals": 1}})
                # Отправка уведомления рефереру о новом реферале
                referrer_data = users_collection.find_one({"id": referrer_id})
                if referrer_data:
                    referrer_name = referrer_data['first_name']
                    referrer_username = referrer_data['username']
                    referrals_count = referrer_data['referrals']
                    message_text = f"""🎉 У вас новый реферал! {referrer_name} (@{referrer_username})

Вам начислено +10 $FRFL!!!!
Всего рефералов: {referrals_count}"""
                    bot.send_message(referrer_id, message_text)

                # Начисление 10 очков репутации за нового реферала
                users_collection.update_one({"id": referrer_id}, {"$inc": {"reputation": 10}})

        # Удаление кнопки "Проверить"
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="Спасибо за подписку! Добро пожаловать!", reply_markup=None)
    else:
        # Удаление сообщения с запросом подписаться и отправка нового сообщения
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="Чтобы продолжить, сначала подпишитесь на наш канал и на наш чат", reply_markup=клавиатура_inline)



# Обработчик нажатия на кнопку "О нас"
@bot.message_handler(func=lambda message: message.text == "О нас 🌐")
def about_us(message):
    # Текст приветствия и информация о сообществе
    about_text = ("Приветствуем тебя в нашем комьюнити крипто-энтузиастов!\n\n"
                  "Мы ищем активных участников, готовых вкладывать свое время и энергию в наше сообщество, чтобы вместе стремиться к успеху!\n\n"
                  "Прежде чем присоединиться к нам, подпишись на наш Telegram-канал и создай свой профиль в этом боте.\n\n"
                  "Здесь ты сможешь отслеживать свой прогресс, получать награды и поощрения от FireFly Crypto! Давай двигаться к успеху вместе!")

    # Создание инлайн кнопок
    keyboard = types.InlineKeyboardMarkup()
    btn_agava_crypto = types.InlineKeyboardButton("FireFly Crypto", url="https://t.me/fireflycomm")
    btn_agava_crypto_chat = types.InlineKeyboardButton("FireFly Crypto Chat", url="https://t.me/+TIBhBif_kQYxZjM0")
    
    # Добавление кнопок на клавиатуру
    keyboard.row(btn_agava_crypto)
    keyboard.row(btn_agava_crypto_chat)

    # Отправка сообщения с текстом и инлайн кнопками
    bot.send_message(message.chat.id, about_text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Профиль 👤")
def profile(message):
    user_id = message.chat.id

    # Получаем данные пользователя из коллекции users
    user_data = users_collection.find_one({"_id": str(user_id)})

    if user_data:
        # Получаем информацию о пользователе из базы данных
        username = user_data.get('username', 'Нет')
        role_name = user_data.get('roles', [{'role_name': 'Newbie'}])[0]['role_name']  # По умолчанию 'Newbie'
        reputation = user_data.get('reputation', 0)
        balance = user_data.get('balance', 0)
        improvements_count = len(user_data.get('improvements', {}))
        tasks_completed_count = len(user_data.get('tasks_completed', []))

        # Формируем сообщение профиля
        profile_message = f"*Имя*: {username}\n"\
                          f"*Username*: @{username}\n"\
                          f"*Роль*: {role_name}\n"\
                          f"*Репутация*: {reputation}\n"\
                          f"*Баланс $FRFL*: {balance}\n"\
                          f"*Куплено улучшений*: {improvements_count}\n"\
                          f"*Выполнено заданий*: {tasks_completed_count}"

        # Создаем клавиатуру для заданий
        tasks_keyboard = types.InlineKeyboardMarkup(row_width=1)
        task_button = types.InlineKeyboardButton("Задания 🎯 ", callback_data="profile_tasks")
        tasks_keyboard.add(task_button)

        bot.send_photo(user_id, media.profile_img, caption=profile_message, reply_markup=tasks_keyboard, parse_mode='Markdown')
    else:
        bot.send_message(user_id, "Вы еще не зарегистрированы")


@bot.callback_query_handler(func=lambda call: call.data == "profile_tasks")
def profile_tasks_handler(call):
    # Создаем клавиатуру для заданий
    tasks_keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    # Кнопка для проверки 10 сообщений в чате
    button_10_messages = types.InlineKeyboardButton("10 сообщений в чате", callback_data="check_10_messages")
    tasks_keyboard.add(button_10_messages)
    
    # Кнопка для проверки 30 сообщений в чате
    button_30_messages = types.InlineKeyboardButton("30 сообщений в чате", callback_data="check_30_messages")
    tasks_keyboard.add(button_30_messages)
    
    # Кнопка для проверки 5 рефералов
    button_5_referrals = types.InlineKeyboardButton("5 рефералов", callback_data="check_5_referrals")
    tasks_keyboard.add(button_5_referrals)
    
    # Кнопка для закрытия сообщения
    button_close = types.InlineKeyboardButton("Закрыть", callback_data="close")
    tasks_keyboard.add(button_close)

    # Отправляем сообщение пользователю
    bot.send_message(call.message.chat.id, "Выполняй задания и зарабатывай $FRFL", reply_markup=tasks_keyboard)


def add_completed_task(user_id, task_name):
    tasks_collection.update_one({"user_id": user_id, "task_name": task_name}, {"$set": {"user_id": user_id, "task_name": task_name}}, upsert=True)

def check_task_completed(user_id, task_name):
    return tasks_collection.find_one({"user_id": user_id, "task_name": task_name}) is not None

@bot.callback_query_handler(func=lambda call: call.data == "check_10_messages")
def check_10_messages_handler(call):
    user_id = call.from_user.id

    # Получаем данные о пользователе из коллекции users_stats
    user_stats_data = users_stats_collection.find_one({'user_id': user_id})

    if user_stats_data:
        message_count = user_stats_data.get("message_count", 0)

        if message_count >= 10 and not check_task_completed(user_id, "check_10_messages"):
            # Логика для обновления очков репутации пользователя в базе данных
            users_collection.update_one({"id": user_id}, {"$inc": {"reputation": 50}})
            add_completed_task(user_id, "check_10_messages")  # Добавляем задание в список выполненных
            bot.answer_callback_query(call.id, text="Вы получили +50 токенов", show_alert=True)
        elif check_task_completed(user_id, "check_10_messages"):
            bot.answer_callback_query(call.id, text="Это задание уже выполнено", show_alert=True)
        else:
            bot.answer_callback_query(call.id, text="У вас недостаточно сообщений в чате", show_alert=True)
    else:
        bot.answer_callback_query(call.id, text="Пользователь не найден в базе данных", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "check_30_messages")
def check_30_messages_handler(call):
    user_id = call.from_user.id

    # Получаем данные о пользователе из коллекции users_stats
    user_stats_data = users_stats_collection.find_one({'user_id': user_id})

    if user_stats_data:
        message_count = user_stats_data.get("message_count", 0)

        if message_count >= 30 and not check_task_completed(user_id, "check_30_messages"):
            # Логика для обновления очков репутации пользователя в базе данных
            users_collection.update_one({"id": user_id}, {"$inc": {"reputation": 100}})
            add_completed_task(user_id, "check_30_messages")  # Добавляем задание в список выполненных
            bot.answer_callback_query(call.id, text="Вы получили +100 токенов", show_alert=True)
        elif check_task_completed(user_id, "check_30_messages"):
            bot.answer_callback_query(call.id, text="Это задание уже выполнено", show_alert=True)
        else:
            bot.answer_callback_query(call.id, text="У вас недостаточно сообщений в чате", show_alert=True)
    else:
        bot.answer_callback_query(call.id, text="Пользователь не найден в базе данных", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "check_5_referrals")
def check_5_referrals_handler(call):
    user_id = call.from_user.id

    # Получаем данные о пользователе из коллекции users
    user_data = users_collection.find_one({'id': user_id})

    if user_data:
        ref_count = user_data.get("referrals", 0)

        if ref_count >= 5 and not check_task_completed(user_id, "check_5_referrals"):
            # Логика для обновления очков репутации пользователя в базе данных
            users_collection.update_one({"id": user_id}, {"$inc": {"reputation": 100}})
            add_completed_task(user_id, "check_5_referrals")  # Добавляем задание в список выполненных
            bot.answer_callback_query(call.id, text="Вы получили +100 токенов", show_alert=True)
        elif check_task_completed(user_id, "check_5_referrals"):
            bot.answer_callback_query(call.id, text="Это задание уже выполнено", show_alert=True)
        else:
            bot.answer_callback_query(call.id, text="У вас недостаточно рефераллов", show_alert=True)
    else:
        bot.answer_callback_query(call.id, text="Пользователь не найден в базе данных", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data == "close")
def close_handler(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)  # Подождите 5 секунд перед повторной попыткой
