from admin_commands import *
from database import connect_to_database
from tasks import task_callback_handler, check_invited_referrals_handler, generate_tasks_keyboard
from markups import *
import telebot
from telebot import types
import pymongo
import os
from datetime import datetime
import time
import random
import string
import media

# Загрузка переменных окружения из файла .env
from dotenv import load_dotenv
load_dotenv()

# Получение коллекций базы данных
chat_stats_collection, users_collection = connect_to_database()

# Ваш бот
token = os.getenv('TELEGRAM_BOT_TOKEN_MAIN')
bot = telebot.TeleBot(token)

# ID вашего канала
chan_id = -1002109241014

# Функция для проверки подписки пользователя на каналы
def check_subscription(user_id):
    try:
        # Проверяем статус участия пользователя в канале
        status = bot.get_chat_member(chan_id, user_id).status
        # Если статус "member", "creator" или "administrator", значит пользователь имеет доступ
        return status in ["member", "creator", "administrator"]
    except Exception as e:
        print("Ошибка при проверке подписки на канал:", e)
        return False

# Функция для генерации случайного реферрального кода
def generate_referral_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Функция для создания профиля пользователя
def create_user_profile(user_id, referrer_id=None):
    username = bot.get_chat(user_id).username
    first_name = bot.get_chat(user_id).first_name
    last_name = bot.get_chat(user_id).last_name
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    referral_code = generate_referral_code()
    referral_link = f"t.me/FireFlyCCbot?start={referral_code}"
    user = {
        "_id": str(user_id),
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "is_admin": 0, 
        "is_registered": True,
        "registration_date": registration_date,
        "email": "",  
        "referral_code": referral_code,
        "referral_link": referral_link,
        "referral_count": 0,
        "balance": 0,  
        "reputation": 0,
        "message_cost": 0.5,
        "improvements": {},  
        "tasks_completed": [],  
        "roles": [{
            "role_id": "Newbie",
            "role_name": "Glowworm Apprentice",
            "description": "Ученик Сияющего Червяка - новый участник, только начинающий свой путь в мире криптовалют и чата 'Firefly Crypto'."
        }]
    }
    if referrer_id:
        user['referrer_id'] = referrer_id
    users_collection.insert_one(user)
    return user

# Функция для обработки нажатия кнопки "Проверить"
@bot.callback_query_handler(func=lambda call: call.data == "check")
def c_listener(call):
    user_id = call.message.chat.id
    is_subscribed = check_subscription(user_id)

    if is_subscribed:
        # Пользователь подписан на каналы, разрешаем ему использовать бота
        bot.send_message(chat_id=user_id, text="Спасибо за подписку! Добро пожаловать!", reply_markup=main_keyboard)

        # Получаем информацию о пользователе из базы данных
        user_data = users_collection.find_one({"_id": str(user_id)})
        if user_data and 'referrer_id' in user_data:
            referrer_id = user_data['referrer_id']
            # Находим информацию о реферере в базе данных по его referrer_code
            referrer_data = users_collection.find_one({"referral_code": referrer_id})
            if referrer_data:
                referrer_id = referrer_data['_id']
                # Отправляем уведомление рефереру о новом реферале
                referrer_name = referrer_data['first_name']
                referrer_username = referrer_data['username']
                message_text = f"""🎉 У вас новый реферал! {referrer_name} (@{referrer_username})

Вам начислено +10 $FRFL!!!!"""
                bot.send_message(referrer_id, message_text)
                # Начисляем 10 очков репутации за нового реферала
                users_collection.update_one({"_id": referrer_id}, {"$inc": {"balance": 10, "referral_count": 1}})
    else:
        # Пользователь не подписан на каналы, предлагаем ему btn_subscribe
        bot.send_message(chat_id=user_id, text="Чтобы продолжить, сначала подпишитесь на наш канал и наш чат", reply_markup=subscribe_keyboard)

# Обработчик команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id

    # Проверяем, зарегистрирован ли уже пользователь
    user_data = users_collection.find_one({"_id": str(user_id)})
    if not user_data:
        # Проверяем, передан ли реферальный код в команде "/start"
        referrer_id = None
        parts = message.text.split()
        if len(parts) > 1:
            referrer_id = parts[1]

        # Создаем профиль пользователя с передачей referrer_id
        create_user_profile(user_id, referrer_id)
        # Отправляем сообщение о подписке и кнопку профиля
        bot.send_message(user_id, f"Добро пожаловать в мир FireFly Crypto!")
        bot.send_message(user_id, """Приветствуем тебя в нашем комьюнити крипто-энтузиастов!

Мы ищем активных участников, готовых вкладывать свое время и энергию в наше сообщество, чтобы вместе стремиться к успеху!

Прежде чем присоединиться к нам, подпишись на наш Telegram-канал и создай свой профиль в этом боте.

Здесь ты сможешь отслеживать свой прогресс, получать награды и поощрения от FireFly Crypto! Давай двигаться к успеху вместе!""", reply_markup=subscribe_keyboard)
    else:
        # Отправляем приветственное сообщение
        bot.send_message(user_id, "С возвращением!", reply_markup=main_keyboard)

# Обработчик нажатия на кнопку "О нас"
@bot.message_handler(func=lambda message: message.text == "О нас 🌐")
def about_us(message):
    # Текст приветствия и информация о сообществе
    about_text = ("Приветствуем тебя в нашем комьюнити крипто-энтузиастов!\n\n"
                  "Мы ищем активных участников, готовых вкладывать свое время и энергию в наше сообщество, чтобы вместе стремиться к успеху!\n\n"
                  "Прежде чем присоединиться к нам, подпишись на наш Telegram-канал и создай свой профиль в этом боте.\n\n"
                  "Здесь ты сможешь отслеживать свой прогресс, получать награды и поощрения от FireFly Crypto! Давай двигаться к успеху вместе!")

    # Отправка сообщения с текстом и инлайн кнопками
    bot.send_message(message.chat.id, about_text, reply_markup=about_us_keyboard)

@bot.message_handler(func=lambda message: message.text == "Профиль 👤")
def profile(message):
    user_id = message.chat.id

    # Получаем данные пользователя из коллекции users
    user_data = users_collection.find_one({"_id": str(user_id)})

    if user_data:
        # Получаем информацию о пользователе из базы данных
        firsr_name = user_data.get('first_name', 'Нет')
        username = user_data.get('username', 'Нет')
        role_id = user_data.get('roles', [{'role_id': 'Newbie'}])[0]['role_id']  # По умолчанию 'Newbie'
        reputation = user_data.get('reputation', 0)
        balance = user_data.get('balance', 0)

        # Формируем сообщение профиля
        profile_message = f"*Имя*: {firsr_name}\n"\
                          f"*Username*: @{username}\n"\
                          f"*Роль*: {role_id}\n"\
                          f"*Репутация*: {reputation}\n\n"\
                          f"*Баланс $FRFL*: {balance}\n"

        bot.send_photo(user_id, media.profile_img, caption=profile_message, reply_markup=profile_keyboard, parse_mode='Markdown')
    else:
        bot.send_message(user_id, "Вы еще не зарегистрированы")
        

@bot.callback_query_handler(func=lambda call: call.data == "profile_stats")
def profile_stats_handler(call):
    try:
        user_id = call.message.chat.id

        # Получаем данные пользователя из коллекции users
        user_data = users_collection.find_one({"_id": str(user_id)})

        if user_data:
            # Инициализируем переменную для общего количества сообщений
            total_messages_count = 0

            # Формируем сообщение со статистикой
            stats_message = f"*Ваша статистика*:\n\n"

            # Проходим по каждому чату
            for chat_stats_data in chat_stats_collection.find():
                chat_title = chat_stats_data.get("chat_title", "Нет данных")
                chat_messages_count = chat_stats_data.get("users", {}).get(str(user_id), {}).get("message_count", 0)
                total_messages_count += chat_messages_count
                chat_percentage = (chat_messages_count / chat_stats_data.get("total_messages_count", 1)) * 100
                stats_message += f"- *{chat_title}*: {chat_messages_count} сообщений ({chat_percentage:.2f}%)\n"

            # Получаем количество купленных улучшений и выполненных заданий
            improvements_count = len(user_data.get('improvements', {}))
            tasks_completed_count = len(user_data.get('tasks_completed', []))
            message_cost = user_data.get('message_cost', 0)

            # Добавляем информацию о купленных улучшениях и выполненных заданиях в сообщение
            stats_message += f"\n\n*Общее количество сообщений*: {total_messages_count}\n"
            stats_message += f"*Количество купленных улучшений*: {improvements_count}\n"
            stats_message += f"*Количество выполненных заданий*: {tasks_completed_count}\n"
            stats_message += f"*Стоимость сообщений*: {message_cost} FRFL"

            bot.send_message(user_id, stats_message, reply_markup=close_keyboard, parse_mode='Markdown')
        else:
            bot.send_message(user_id, "Данные пользователя отсутствуют")
    except Exception as e:
        print("Error handling profile_stats command:", e)

# Обработчик для кнопки "Реферральная программа"
@bot.callback_query_handler(func=lambda call: call.data == "ref_program")
def referral_program_handler(call):
    try:
        user_id = call.message.chat.id

        # Получаем данные пользователя из коллекции users
        user_data = users_collection.find_one({"_id": str(user_id)})

        if user_data:
            # Формируем реферальную ссылку
            referral_link = user_data['referral_link']
            referral_count = user_data.get("referral_count", 0)

            # Формируем текст сообщения для отправки в чате
            reply_text_chat = (
                "🌟 *Реферральная программа*\n\n"
                "Пригласи друзей и получи бонусы!\n\n"
                f"👥 *Количество приглашенных друзей*: {referral_count}\n"
                "💰 *Бонусы*: За каждого приглашенного друга вы получаете бонусные токены!\n"
                "📎 *Условия*: Условия реферральной программы можно узнать у администратора.\n\n"
                f"*Ваша реферральная ссылка*: {referral_link}"
            )

            # Формируем текст сообщения для отправки другу
            reply_text_friend = (
                "Привет! Я приглашаю тебя присоединиться к боту FireFly Crypto. \n\n"
                "С ним ты можешь зарабатывать крипту за общение в чате! \n\n"
                f"Вот моя реферальная ссылка для регистрации: {referral_link}"
            )

            # Отправляем сообщение с инлайн-клавиатурой в чат
            bot.send_message(chat_id=user_id, text=reply_text_chat, reply_markup=generate_ref_keyboard(reply_text_friend), parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.send_message(chat_id=user_id, text="Вы еще не зарегистрированы")
    except Exception as e:
        print("Error handling ref_program callback:", e)

# Обработчик для кнопки "Мои приглашенные друзья"
@bot.callback_query_handler(func=lambda call: call.data == "my_ref_friends")
def my_referral_friends_handler(call):
    try:
        user_id = call.message.chat.id

        # Получаем данные пользователя из коллекции users
        user_data = users_collection.find_one({"_id": str(user_id)})

        if user_data:
            # Получаем referral_code пользователя
            referral_code = user_data.get("referral_code")

            # Ищем всех пользователей, чей referrer_id совпадает с referral_code текущего пользователя
            referred_users = users_collection.find({"referrer_id": referral_code})

            # Формируем текст сообщения со списком приглашенных друзей
            referral_friends_message = "*Список приглашенных друзей*:\n\n"
            for referred_user in referred_users:
                # Извлекаем имя и username приглашенного друга
                first_name = referred_user.get("first_name", "")
                username = referred_user.get("username", "")
                # Добавляем информацию о приглашенном друге в текст сообщения
                referral_friends_message += f"*Друг: {first_name} (@{username})*\n"

            # Отправляем сообщение с информацией о приглашенных друзьях
            bot.send_message(chat_id=user_id, text=referral_friends_message, parse_mode="Markdown", reply_markup=close_keyboard)
        else:
            bot.send_message(chat_id=user_id, text="Вы еще не зарегистрированы")
    except Exception as e:
        print("Error handling my_ref_friends callback:", e)


# Удаляет последнее отправленное сообщение 
@bot.callback_query_handler(func=lambda call: call.data == "close")
def close_message_handler(call):
    # Удаляем сообщение с клавиатурой
    bot.delete_message(call.message.chat.id, call.message.message_id) 

# Обработчик клавиатуры для заданий
@bot.callback_query_handler(func=lambda call: call.data == "profile_tasks")
def profile_tasks_handler(call):
    profile_keyboard = generate_tasks_keyboard()
    bot.send_message(call.message.chat.id, "Выполняй задания и зарабатывай $FRFL", reply_markup=profile_keyboard)

# Обработчики команд для заданий
@bot.callback_query_handler(func=lambda call: call.data == "check_10_messages")
def check_10_messages_callback(call):
    task_callback_handler(bot, call, users_collection, chat_stats_collection, "task_id_10_messages", 10, 50)


@bot.callback_query_handler(func=lambda call: call.data == "check_30_messages")
def check_30_messages_callback(call):
    task_callback_handler(bot, call, users_collection, chat_stats_collection, "task_id_30_messages", 30, 100)

@bot.callback_query_handler(func=lambda call: call.data == "check_invited_referrals")
def check_invited_referrals_callback(call):
    check_invited_referrals_handler(bot, call, users_collection)

# Ваш файл с обработчиками команд админов
@bot.message_handler(commands=['givebalance'])
def handle_give_balance_command(message):
    execute_give_balance_command(bot, message, *message.text.split()[1:], users_collection)

@bot.message_handler(commands=['giverep'])
def handle_give_reputation_command(message):
    execute_give_reputation_command(bot, message, *message.text.split()[1:], users_collection)

@bot.message_handler(commands=['giveref'])
def handle_give_referral_count_command(message):
    execute_give_referral_count_command(bot, message, *message.text.split()[1:], users_collection)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)  # Подождите 5 секунд перед повторной попыткой
