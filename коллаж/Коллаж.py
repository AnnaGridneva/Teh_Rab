import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
import tkinter as tk
from tkinter import filedialog, messagebox

imgs = []
def get_imgs(folder, exts):
    # Получение списка изображений в указанной папке с допустимыми расширениями
    imgs = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    # Проверка на наличие изображений и отображение ошибки, если их нет
    if not imgs:
        messagebox.showerror("Ошибка", "Нет изображений с выбранными расширениями.")
        return []
    # Очистка текущего списка 
    listbox.delete(0, tk.END)
    # Добавление найденных изображений в список
    for img in imgs:
        listbox.insert(tk.END, img)
    return imgs

def gen_collage(folder, title, out_file, img_size=(150, 150), border=5):
    # Генерация коллажа из выбранных изображений
    if not imgs:
        # Ошибка, если не выбрано изображение
        messagebox.showerror("Ошибка", "Не выбрано изображение.")
        return
    
    # Загрузка шрифта Arial, иначе использовать стандартный
    try:
        fnt = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        fnt = ImageFont.load_default()
        
    # Общее количество изображений
    n = len(imgs)  
    # Рразмер сетки в коллаже
    grid_size = int(n ** 0.5) + 1
    width = grid_size * (img_size[0] + border) - border  # Ширина коллажа
    height = width + 60  # Высота коллажа с учетом заголовка
    
    # Создание нового изображения коллажа с серым фоном
    collage = Image.new('RGB', (width, height), color=(220, 220, 220))
    
    x, y = 0, 60  # Начальные координаты для размещения изображений
    for i, img_name in enumerate(imgs):
        img_path = os.path.join(folder, img_name)  # Путь к изображению
        
        # Проверка существования файла, если нет - ошибка
        if not os.path.exists(img_path):
            messagebox.showerror("Ошибка", f"Файл не найден: {img_path}")
            return
        
        # Попытка открыть и изменить размер изображения
        try:
            img = Image.open(img_path)  # Открытие изображения
            img = ImageOps.fit(img, img_size, method=Image.LANCZOS)  # Изменение размера
        except Exception as e:
            # Обработка ошибки при открытии
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {img_path}\n{str(e)}")
            return
        
        # Размещение рамки и изображения в коллаже
        collage.paste((0, 0, 0), (x, y, x + img_size[0] + border, y + img_size[1] + border))
        collage.paste(img, (x + border // 2, y + border // 2))  # Позиционирование изображения
        x += img_size[0] + border  # Сдвиг по горизонтали
        
        # Если достигнут конец строки - сдвиг по вертикали
        if (i + 1) % grid_size == 0:
            x = 0
            y += img_size[1] + border
    
    # Добавление заголовка к изображению коллажа
    draw = ImageDraw.Draw(collage)  # Создание объекта для рисования
    text_bbox = draw.textbbox((0, 0), title, font=fnt)  # Получение границ текста
    text_width = text_bbox[2] - text_bbox[0]  # Ширина текста
    draw.text(((width - text_width) // 2, 30), title, font=fnt, fill=(0, 0, 0))  # Рисование текста
    
    # Сохранение итогового коллажа
    collage.save(out_file, 'JPEG')
    # Уведомление пользователя о завершении
    messagebox.showinfo("Готово", f"Коллаж сохранен как '{out_file}'")

def load_imgs():
    # Выбор папки для загрузки изображений от пользователя
    folder = filedialog.askdirectory(title="Выберите папку с изображениями")
    
    # Проверка, была ли выбрана папка
    if not folder:
        return
    
    # Введенные пользователем расширения
    exts = entry_ext.get().strip().split(',')
    # Формирование кортежа допустимых расширений
    exts = tuple('.' + ext.strip().lower() for ext in exts)
    
    global imgs
    # Загрузка изображений с указанными параметрами
    imgs = get_imgs(folder, exts)

def save_collage():
    # Сохранение коллажа в указанное пользователем место
    if not imgs:
        # Ошибка, если не выбраны изображения
        messagebox.showerror("Ошибка", "Сначала выберите изображения.")
        return
    out_file = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
    
    # Если выбран файл, генерируем коллаж
    if out_file:
        title = entry_title.get() 
        gen_collage(os.path.dirname(out_file), title, out_file) 

# Создание главного окна
root = tk.Tk() 
root.title("Генератор коллажа")  
# Поля ввода 
tk.Label(root, text="Введите расширения изображений (например, jpg, png):").pack(pady=5)
# Ввод расширений
entry_ext = tk.Entry(root, width=40)
entry_ext.pack(pady=5)
tk.Label(root, text="Введите заголовок для коллажа:").pack(pady=5)
# Ввод заголовка
entry_title = tk.Entry(root, width=40)
entry_title.pack(pady=5)
# Кнопка для загрузки изображений
btn_load = tk.Button(root, text="Выберите папку", command=load_imgs) 
btn_load.pack(pady=20)
# Список для отображения выбранных изображений
listbox = tk.Listbox(root, width=50, selectmode=tk.MULTIPLE) 
listbox.pack(pady=10)
# Кнопка для сохранения коллажа
btn_save = tk.Button(root, text="Сохранить коллаж", command=save_collage)  
btn_save.pack(pady=10)
# Запуск цикла
root.mainloop()  
