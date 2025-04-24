import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont
import random

class MemeGen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Meme Generator")
        self.root.config(bg="#2b2b2b")
        
        #Подсказоки для текста
        self.top_texts = [
            "Я проснулся",
            "Я съел",
            "Я увидел",
            "Я услышал",
            "Я почувствовал",
            "Я понял",
            "Я сделал",
            "Я нашел",
            "Я потерял",
            "Я забыл"
        ]
        
        self.bottom_texts = [
            "и теперь я богат",
            "и теперь я счастлив",
            "и теперь я мем",
            "и теперь я свободен",
            "и теперь я сильнее",
            "и теперь я умнее",
            "и теперь я красивее",
            "и теперь я успешнее",
            "и теперь я знаменит",
            "и теперь я легенда"
        ]
        
        #Для верхнего текста
        top_frame = tk.Frame(self.root, bg="#2b2b2b")
        top_frame.pack(pady=10)
        
        # Кнопка для выбора изображения
        self.img_btn = tk.Button(top_frame, text="Выбрать изображение", bg="#4b4b4b", fg="white", command=self.select_img)
        self.img_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для выбора папки для сохранения
        self.save_btn = tk.Button(top_frame, text="Куда сохранить", bg="#4b4b4b", fg="white", command=self.select_save_folder)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        #Для полей текста
        text_frame = tk.Frame(self.root, bg="#2b2b2b")
        text_frame.pack(pady=10)
        
        #Для верхнего текста с подсказкой
        self.top_label = tk.Label(text_frame, text="Верхний текст:", bg="#2b2b2b", fg="white")
        self.top_label.pack()
        self.top_entry = tk.Entry(text_frame, width=50)
        self.top_entry.insert(0, random.choice(self.top_texts))
        self.top_entry.pack()
        self.top_change_btn = tk.Button(text_frame, text="Сменить", bg="#4b4b4b", fg="white", command=self.change_top_text)
        self.top_change_btn.pack()
        
        #Для нижнего текста с подсказкой
        self.bottom_label = tk.Label(text_frame, text="Нижний текст:", bg="#2b2b2b", fg="white")
        self.bottom_label.pack()
        self.bottom_entry = tk.Entry(text_frame, width=50)
        self.bottom_entry.insert(0, random.choice(self.bottom_texts))
        self.bottom_entry.pack()
        self.bottom_change_btn = tk.Button(text_frame, text="Сменить", bg="#4b4b4b", fg="white", command=self.change_bottom_text)
        self.bottom_change_btn.pack()
        
        #Для настроеки текста
        settings_frame = tk.Frame(self.root, bg="#2b2b2b")
        settings_frame.pack(pady=10)
        
        #Кнопка для выбора цвета текста
        self.color_btn = tk.Button(settings_frame, text="Цвет текста", bg="#4b4b4b", fg="white", command=self.select_color)
        self.color_btn.pack(side=tk.LEFT, padx=5)
        
        #Кнопка для изменения размера текста
        self.size_btn = tk.Button(settings_frame, text="Размер текста", bg="#4b4b4b", fg="white", command=self.change_size)
        self.size_btn.pack(side=tk.LEFT, padx=5)
        
        #Кнопка для добавления рамки
        self.border_btn = tk.Button(settings_frame, text="Добавить рамку", bg="#4b4b4b", fg="white", command=self.add_border)
        self.border_btn.pack(side=tk.LEFT, padx=5)
        
        #Кнопка для генерации мема
        self.gen_btn = tk.Button(self.root, text="Сгенерировать мем", bg="#4b4b4b", fg="white", command=self.generate_meme)
        self.gen_btn.pack(pady=20)
        
        self.img_path = None
        self.text_color = (255, 255, 255)
        self.font_size = 20
        self.save_folder = "."
        self.border = False

    def select_img(self):
        self.img_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png")])
        
    def select_color(self):
        self.text_color = colorchooser.askcolor(title="Выберите цвет текста")[0]
        
    def generate_meme(self):
        if self.img_path:
            img = Image.open(self.img_path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("arial.ttf", self.font_size)
            
            #Добавление верхнего текста
            top_text = self.top_entry.get()
            draw.text((10, 10), top_text, fill=self.text_color, font=font)
            
            #Добавление нижнего текста
            bottom_text = self.bottom_entry.get()
            draw.text((10, img.height - 30), bottom_text, fill=self.text_color, font=font)
            
            #Добавление рамки
            if self.border:
                draw.rectangle([(0, 0), (img.width - 1, img.height - 1)], outline=(255, 255, 255), width=5)
            
            #Сохранение мема
            img.save(f"{self.save_folder}/meme.png")
            print(f"Мем сгенерирован и сохранен в {self.save_folder}/meme.png")
        else:
            print("Выберите изображение")

    def add_border(self):
        self.border = not self.border
        if self.border:
            self.border_btn.config(text="Удалить рамку")
        else:
            self.border_btn.config(text="Добавить рамку")
            
    def change_size(self):
        size_window = tk.Toplevel(self.root)
        size_label = tk.Label(size_window, text="Введите размер текста:")
        size_label.pack()
        size_entry = tk.Entry(size_window)
        size_entry.pack()
        
        def set_size():
            try:
                new_size = int(size_entry.get())
                if new_size > 0:
                    self.font_size = new_size
                size_window.destroy()
            except ValueError:
                print("Введите корректный размер текста!")
                
        size_btn = tk.Button(size_window, text="Установить размер", command=set_size)
        size_btn.pack()

    def select_save_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.save_folder = folder_path
        
    def change_top_text(self):
        new_top_text = random.choice(self.top_texts)
        self.top_entry.delete(0, tk.END)
        self.top_entry.insert(0, new_top_text)

    def change_bottom_text(self):
        new_bottom_text = random.choice(self.bottom_texts)
        self.bottom_entry.delete(0, tk.END)
        self.bottom_entry.insert(0, new_bottom_text)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MemeGen()
    app.run()
