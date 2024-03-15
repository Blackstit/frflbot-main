from database import connect_to_database
from telebot import types

chat_stats_collection, users_collection = connect_to_database()

# Создаем клавиатуру 
def generate_tasks_keyboard():
    tasks_keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    button_10_messages = types.InlineKeyboardButton("10 сообщений в чате", callback_data="check_10_messages")
    tasks_keyboard.add(button_10_messages)
    
    button_30_messages = types.InlineKeyboardButton("30 сообщений в чате", callback_data="check_30_messages")
    tasks_keyboard.add(button_30_messages)
    
    button_5_referrals = types.InlineKeyboardButton("5 рефералов", callback_data="check_5_referrals")
    tasks_keyboard.add(button_5_referrals)
    
    button_close = types.InlineKeyboardButton("Закрыть ❌", callback_data="close")
    tasks_keyboard.add(button_close)

    return tasks_keyboard

def add_completed_task(user_id, task_id, task_name, reward):
    task = {
        "task_id": task_id,
        "task_name": task_name,
        "reward": reward
    }
    users_collection.update_one({"_id": str(user_id)}, {"$push": {"tasks_completed": task}})

def check_task_completed(user_id, task_id, users_collection):
    user_data = users_collection.find_one({"_id": user_id})
    if user_data:
        tasks_completed = user_data.get('tasks_completed', [])
        for task in tasks_completed:
            if task['task_id'] == task_id:
                return True
    return False

def task_callback_handler(bot, call, users_collection, chat_stats_collection, task_id, min_messages, reward):
    user_id = str(call.from_user.id)  # Приводим к строковому значению

    # Получаем все документы из коллекции chat_stats
    all_chat_stats = chat_stats_collection.find()
    total_message_count = 0

    # Проходим по каждому документу
    for chat_stats_data in all_chat_stats:
        if 'users' in chat_stats_data:
            # Получаем статистику сообщений для данного пользователя
            user_stats = chat_stats_data['users'].get(user_id, {})
            total_message_count += user_stats.get("message_count", 0)

    # Проверяем, выполнено ли задание
    if check_task_completed(user_id, task_id, users_collection):
        bot.answer_callback_query(call.id, text="Это задание уже выполнено", show_alert=True)
        return

    if total_message_count >= min_messages:
        # Логика для обновления очков репутации пользователя в базе данных
        users_collection.update_one({"_id": user_id}, {"$inc": {"reputation": reward}})
        add_completed_task(user_id, task_id, f"{min_messages} сообщений в чате", reward)  # Добавляем задание в список выполненных
        bot.answer_callback_query(call.id, text=f"Вы получили +{reward} токенов", show_alert=True)
    else:
        bot.answer_callback_query(call.id, text="У вас недостаточно сообщений в чате", show_alert=True)

def check_invited_referrals_handler(bot, call, users_collection):
    user_id = str(call.from_user.id)  # Приводим к строковому значению

    # Получаем данные о пользователе из коллекции users
    user_data = users_collection.find_one({"_id": user_id})
    if user_data:
        invited_referrals_count = len(user_data.get("invited_referrals", []))

        # Проверяем, выполнено ли задание
        if check_task_completed(user_id, "task_id_invited_referrals", users_collection):
            bot.answer_callback_query(call.id, text="Это задание уже выполнено", show_alert=True)
            return

        if invited_referrals_count >= 5:
            # Логика для обновления очков репутации пользователя в базе данных
            users_collection.update_one({"_id": user_id}, {"$inc": {"reputation": 100}})
            add_completed_task(user_id, "task_id_invited_referrals", "5 приглашенных рефералов", 100)  # Добавляем задание в список выполненных
            bot.answer_callback_query(call.id, text="Вы получили +100 токенов", show_alert=True)
        else:
            bot.answer_callback_query(call.id, text="У вас недостаточно приглашенных рефералов", show_alert=True)
    else:
        bot.answer_callback_query(call.id, text="Пользователь не найден в базе данных", show_alert=True)

