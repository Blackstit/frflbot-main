from database import connect_to_database
from dotenv import load_dotenv
load_dotenv()


chat_stats_collection, users_collection = connect_to_database()

# admin_commands.py
def execute_give_balance_command(bot, message, user_id, amount, users_collection):
    try:
        user_id = str(user_id)  # Преобразуем user_id в строку
        amount = float(amount)
        # Обновляем баланс пользователя в базе данных
        users_collection.update_one({"_id": user_id}, {"$inc": {"balance": amount}})
        bot.reply_to(message, f"Баланс пользователя {user_id} успешно пополнен на {amount}.")
    except ValueError:
        bot.reply_to(message, "Неверный формат параметров. Используйте синтаксис команды: /givebalance <user_id> <количество>")

def execute_give_reputation_command(bot, message, user_id, amount, users_collection):
    try:
        user_id = str(user_id)  # Преобразуем user_id в строку
        amount = int(amount)
        # Обновляем репутацию пользователя в базе данных
        users_collection.update_one({"_id": user_id}, {"$inc": {"reputation": amount}})
        bot.reply_to(message, f"Репутация пользователя {user_id} успешно увеличена на {amount}.")
    except ValueError:
        bot.reply_to(message, "Неверный формат параметров. Используйте синтаксис команды: /giverep <user_id> <количество>")

def execute_give_referral_count_command(bot, message, user_id, amount, users_collection):
    try:
        user_id = str(user_id)  # Преобразуем user_id в строку
        amount = int(amount)
        print("users_collection:", users_collection)  # Добавлено логирование
        print(f"user_id: {user_id} amount: {amount}" )
        # Обновляем количество рефераллов пользователя в базе данных
        users_collection.update_one({"_id": user_id}, {"$inc": {"referral_count": amount}})
        bot.reply_to(message, f"Количество рефераллов пользователя {user_id} успешно увеличено на {amount}.")
    except ValueError:
        bot.reply_to(message, "Неверный формат параметров. Используйте синтаксис команды: /giveref <user_id> <количество>")

def execute_give_admin_command(bot, message, user_id, value, users_collection):
    try:
        user_id = str(user_id)  # Преобразуем user_id в строку
        value = int(value)
        if value not in [0, 1, 2, 3]:
            bot.reply_to(message, "Значение должно быть от 0 до 3.")
            return
        # Логика установки значения is_admin
        users_collection.update_one({"_id": user_id}, {"$set": {"is_admin": value}})
        bot.reply_to(message, f"Пользователю {user_id} установлено значение is_admin: {value}.")
    except ValueError:
        bot.reply_to(message, "Неверный формат параметров. Используйте синтаксис команды: /giveadmin <user_id> <значение>")
