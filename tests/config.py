import os
import logging
from faker import Faker

BASE_URL = "http://localhost:3000/api"
TIMEOUT = 5
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
fake = Faker('ru_RU')

#============================================================================================
# === УМНОЕ ЛОГИРОВАНИЕ (ПАТТЕРН МИДЛА) ===
# 1. Вычисляем абсолютный путь к папке, где лежит этот самый файл config.py
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, "api_tests.log")

# 2. Создаем изолированный объект логгера с уникальным именем
logger = logging.getLogger("api_tests_logger")
logger.setLevel(logging.INFO)

# Очищаем старые обработчики, если они были (защита от дублирования записей)
if logger.hasHandlers():
    logger.handlers.clear()

# 3. Создаем красивый формат для строк лога
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# 4. Создаем обработчик для записи строго в наш файл с кодировкой UTF-8
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# 5. Создаем обработчик для дублирования логов прямо в консоль терминала
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)
#============================================================================================




# Старая простая версия. ( грузит в лог в терминал папку )
# logging.basicConfig(
#     level=logging.INFO,
#     format= "%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[
#         logging.FileHandler("api_tests.log", encoding="utf-8"), # Все логи будут записываться в этот файл
#         logging.StreamHandler() # И параллельно дублироваться в консоль терминала
#     ]
# )

# logger = logging.getLogger("api_tests")