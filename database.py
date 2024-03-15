import pymongo
import os
from dotenv import load_dotenv



# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение переменных окружения для подключения к MongoDB
MONGO_URL = os.getenv("MONGO_URL")

def connect_to_database():
    # Подключение к MongoDB и определение коллекций
    client = pymongo.MongoClient(MONGO_URL)
    db = client['test']

    # users_stats_collection = db.get_collection('users_stats')  # Коллекция для статистики пользователей
    chat_stats_collection = db.get_collection('chat_stats_collection') # Коллекция для статистики чатов и их пользователей
    users_collection = db.get_collection('users')  # Коллекция для пользователей


    return  chat_stats_collection, users_collection

