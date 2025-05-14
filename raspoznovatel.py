import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import easyocr
import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Распознание")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.reader = easyocr.Reader(['ru', 'en'], gpu=False)

        self.frm_pic = tk.Frame(root, width=300, height=350, bg="gray90", relief="sunken", bd=2)
        self.frm_pic.pack(padx=10, pady=10)
        self.frm_pic.pack_propagate(False)

        self.lbl_pic = tk.Label(self.frm_pic, text="Загрузите фото", bg="gray90")
        self.lbl_pic.pack(fill=tk.BOTH, expand=True)

        self.frm_btn = tk.Frame(root)
        self.frm_btn.pack(pady=5)

        self.btn_load = tk.Button(self.frm_btn, text="Загрузить", command=self.load)
        self.btn_load.grid(row=0, column=0, padx=5)

        self.btn_rec = tk.Button(self.frm_btn, text="Распознать", command=self.recognize, state=tk.DISABLED)
        self.btn_rec.grid(row=0, column=1, padx=5)

        self.btn_save = tk.Button(self.frm_btn, text="Сохранить", command=self.save, state=tk.DISABLED)
        self.btn_save.grid(row=0, column=2, padx=5)

        self.txt = tk.Text(root, height=5, wrap=tk.WORD)
        self.txt.pack(fill=tk.X, padx=10, pady=10)

        self.path = None
        self.img = None

    def load(self):
        ftypes = [("Фото", "*.png *.jpg *.jpeg *.bmp"), ("Все", "*.*")]
        p = filedialog.askopenfilename(title="Выбрать фото", filetypes=ftypes)
        if p:
            try:
                im = Image.open(p)
                w, h = im.size
                fw, fh = self.frm_pic.winfo_width(), self.frm_pic.winfo_height()
                if fw == 1 and fh == 1:
                    fw, fh = 300, 350
                r = min(fw / w, fh / h)
                new_size = (int(w * r), int(h * r))
                im = im.resize(new_size, Image.LANCZOS)
                self.img = ImageTk.PhotoImage(im)
                self.lbl_pic.config(image=self.img, text="")
                self.path = p
                self.btn_rec.config(state=tk.NORMAL)
                self.txt.delete(1.0, tk.END)
                self.btn_save.config(state=tk.DISABLED)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не загрузить фото:\n{e}")

    def recognize(self):
        if not self.path:
            messagebox.showwarning("Внимание", "Сначала загрузите фото")
            return
        self.txt.delete(1.0, tk.END)
        try:
            res = self.reader.readtext(self.path, detail=0, paragraph=True)
            txt = "\n".join(res)
            self.txt.insert(tk.END, txt)
            self.btn_save.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def save(self):
        txt = self.txt.get(1.0, tk.END).strip()
        if not txt:
            messagebox.showwarning("Внимание", "Нет текста для сохранения")
            return
        fname = f"txt_{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.txt"
        p = filedialog.asksaveasfilename(defaultextension=".txt",
                                         filetypes=[("Текст", "*.txt"), ("Все", "*.*")],
                                         initialfile=fname,
                                         title="Сохранить файл")
        if p:
            try:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(txt)
                messagebox.showinfo("Готово", f"Сохранено:\n{p}")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
