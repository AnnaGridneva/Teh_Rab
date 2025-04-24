import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.utils import get_color_from_hex
import os
import webbrowser
from PIL import Image as PILImage
from kivy.core.image import Image as CoreImage
import io
from plyer import filechooser
from kivy.config import Config
from kivy.resources import resource_add_path
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window

kivy.require('2.0.0')
Config.set('graphics', 'default_font', ['Roboto', 'data/fonts/Roboto-Regular.ttf', 'data/fonts/Roboto-Italic.ttf', 'data/fonts/Roboto-Bold.ttf', 'data/fonts/Roboto-BoldItalic.ttf'])
Config.set('graphics', 'resizable', 0)  

class DrawingWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_width = 2 
        self.line_color = (0, 0, 0, 1)  
        self.eraser_mode = False  

        with self.canvas:
            Color(1, 1, 1, 1)  
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                if self.eraser_mode:
                    Color(1, 1, 1, 1) 
                else:
                    Color(*self.line_color)

                touch.ud['line'] = Line(points=[touch.x, touch.y], width=self.line_width)
            return True 

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]
            return True

    def set_line_width(self, width):
        self.line_width = width

    def set_line_color(self, color):
        self.line_color = color

    def clear_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)  
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def set_eraser_mode(self, active):
        self.eraser_mode = active

class DrawingToolPopup(Popup):
    def __init__(self, drawing_widget, **kwargs):
        super().__init__(**kwargs)
        self.drawing_widget = drawing_widget
        self.title = "Инструменты рисования"
        self.size_hint = (None, None)
        self.size = (400, 350)  
        self.auto_dismiss = False  
        self.selected_color = drawing_widget.line_color  

        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        width_label = Label(text="Толщина линии:")
        self.width_input = TextInput(text=str(drawing_widget.line_width), input_type='number', size_hint_y=None,
                                      height=30) 
        root_layout.add_widget(width_label)
        root_layout.add_widget(self.width_input)

        color_label = Label(text="Цвет линии:")
        root_layout.add_widget(color_label)
        color_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        red_button = Button(text="Красный", background_color=(1, 0, 0, 1))
        green_button = Button(text="Зеленый", background_color=(0, 1, 0, 1))
        blue_button = Button(text="Синий", background_color=(0, 0, 1, 1))
        black_button = Button(text="Черный", background_color=(0, 0, 0, 1))
        white_button = Button(text="Белый", background_color=(1, 1, 1, 1))

        red_button.bind(on_release=lambda instance: self.set_color((1, 0, 0, 1)))
        green_button.bind(on_release=lambda instance: self.set_color((0, 1, 0, 1)))
        blue_button.bind(on_release=lambda instance: self.set_color((0, 0, 1, 1)))
        black_button.bind(on_release=lambda instance: self.set_color((0, 0, 0, 1)))
        white_button.bind(on_release=lambda instance: self.set_color((1, 1, 1, 1)))

        color_layout.add_widget(red_button)
        color_layout.add_widget(green_button)
        color_layout.add_widget(blue_button)
        color_layout.add_widget(black_button)
        color_layout.add_widget(white_button)

        root_layout.add_widget(color_layout)

        eraser_button = Button(text="Ластик", size_hint_y=None, height=40)
        eraser_button.bind(on_release=self.toggle_eraser)
        root_layout.add_widget(eraser_button)

        apply_button = Button(text="Применить", size_hint_y=None, height=40)
        apply_button.bind(on_release=self.apply_changes)
        root_layout.add_widget(apply_button)

        cancel_button = Button(text="Отмена", size_hint_y=None, height=40)
        cancel_button.bind(on_release=self.dismiss)
        root_layout.add_widget(cancel_button)

        self.content = root_layout

    def set_color(self, color):
        self.selected_color = color

    def toggle_eraser(self, instance):
        self.drawing_widget.set_eraser_mode(not self.drawing_widget.eraser_mode)
        if self.drawing_widget.eraser_mode:
            print("Eraser mode ON")
        else:
            print("Eraser mode OFF")

    def apply_changes(self, instance):
        try:
            width = int(self.width_input.text)
            self.drawing_widget.set_line_width(width)
        except ValueError:
            print("Invalid width value")

        self.drawing_widget.set_line_color(self.selected_color)

        self.dismiss()

class DrawingPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Окно для рисования"
        self.size_hint = (None, None)
        self.size = (800, 600)
        self.drawing_widget = DrawingWidget()

        root_layout = BoxLayout(orientation='vertical')

        root_layout.add_widget(self.drawing_widget)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

        tools_button = Button(text="Инструменты", size_hint_y=None, height=40)
        tools_button.bind(on_release=self.open_drawing_tools)
        button_layout.add_widget(tools_button)

        clear_button = Button(text="Очистить", size_hint_y=None, height=40)
        clear_button.bind(on_release=self.clear_drawing)
        button_layout.add_widget(clear_button)

        save_button = Button(text="Сохранить", size_hint_y=None, height=40)
        save_button.bind(on_release=self.save_drawing)
        button_layout.add_widget(save_button)

        exit_button = Button(text="Выход", size_hint_y=None, height=40)
        exit_button.bind(on_release=self.exit_drawing)
        button_layout.add_widget(exit_button)

        root_layout.add_widget(button_layout)

        self.content = root_layout

    def clear_drawing(self, instance):
        self.drawing_widget.clear_canvas()

    def open_drawing_tools(self, instance):
        self.tools_popup = DrawingToolPopup(self.drawing_widget)
        self.tools_popup.open()

    def save_drawing(self, instance):
        img = self.drawing_widget.export_as_image()
        buffer = io.BytesIO()
        img.save(buffer, fmt='png')
        buffer.seek(0)

        filechooser.save_file(
            title="Сохранить рисунок",
            filters=[("PNG Image", "*.png")],
            on_selection=lambda selection: self.save_to_file(selection, buffer)
        )

    def save_to_file(self, selection, buffer):
        if selection:
            filepath = selection[0]
            if not filepath.endswith('.png'):
                filepath += '.png'
            with open(filepath, 'wb') as f:
                f.write(buffer.read())
            print(f"Рисунок сохранен в {filepath}")

    def exit_drawing(self, instance):
        self.dismiss() 


class QwotaMessenger(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.messages = []
        self.image_references = []

        self.chat_area = ChatArea()
        self.add_widget(self.chat_area)

        control_frame = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        self.message_entry = TextInput(multiline=False)
        self.message_entry.bind(on_text_validate=self.send_message)
        control_frame.add_widget(self.message_entry)

        self.send_button = Button(text="Отправить")
        self.send_button.bind(on_release=self.send_message)
        control_frame.add_widget(self.send_button)

        self.photo_button = Button(text="Фото")
        self.photo_button.bind(on_release=self.send_photo)
        control_frame.add_widget(self.photo_button)

        self.clear_button = Button(text="Очистить")
        self.clear_button.bind(on_release=self.clear_chat)
        control_frame.add_widget(self.clear_button)

        self.drawing_button = Button(text="Рисовать")
        self.drawing_button.bind(on_release=self.open_drawing_popup)
        control_frame.add_widget(self.drawing_button)

        self.add_widget(control_frame)

        self.load_messages()

    def send_message(self, instance):
        message = self.message_entry.text.strip()
        if message:
            self.messages.append({
                "type": "text",
                "content": message,
                "metadata": {"edited": False}
            })
            self.update_chat_area()
            self.message_entry.text = ''
            self.save_messages()

    def send_photo(self, instance):
        try:
            filechooser.open_file(
                title="Выберите изображение",
                filters=[("Images", "*.png;*.jpg;*.jpeg")],
                on_selection=self.on_photo_selected
            )
        except Exception as e:
            print(f"Error opening file chooser: {e}")

    def on_photo_selected(self, selection):
        try:
            if selection and len(selection) > 0:
                photo_path = selection[0]
                self.messages.append({"type": "photo", "content": photo_path, "metadata": {"edited": False}})
                self.update_chat_area()
                self.save_messages()
        except Exception as e:
            print(f"Error processing selected photo: {e}")

    def update_chat_area(self):
        self.chat_area.clear_messages()
        for idx, msg in enumerate(self.messages):
            self.chat_area.add_message(msg, idx, self.show_context_menu)

    def show_context_menu(self, index):
        content = BoxLayout(orientation='vertical')

        if self.messages[index]["type"] == "text":
            edit_button = Button(text="Редактировать")
            edit_button.bind(on_release=lambda instance: self.edit_message(index))
            content.add_widget(edit_button)

            search_button = Button(text="Поиск")
            search_button.bind(on_release=lambda instance: self.search_message(index))
            content.add_widget(search_button)
        else:
            replace_photo_button = Button(text="Заменить фото")
            replace_photo_button.bind(on_release=lambda instance: self.replace_photo(index))
            content.add_widget(replace_photo_button)

        delete_button = Button(text="Удалить")
        delete_button.bind(on_release=lambda instance: self.delete_message(index))
        content.add_widget(delete_button)

        cancel_button = Button(text="Отмена")
        cancel_button.bind(on_release=self.close_popup)
        content.add_widget(cancel_button)

        self.popup = Popup(title='Действия', content=content, size_hint=(None, None), size=(200, 250))
        self.popup.open()

    def search_message(self, index):
        text = self.messages[index]["content"]
        search_url = f"https://yandex.ru/search/?text={text}"
        webbrowser.open(search_url)

    def edit_message(self, index):
        self.popup.dismiss()
        content = BoxLayout(orientation='vertical')
        label = Label(text='Введите новый текст:')
        text_input = TextInput(text=self.messages[index]["content"], multiline=False)
        content.add_widget(label)
        content.add_widget(text_input)
        save_button = Button(text='Сохранить')

        def save_edit(instance):
            new_text = text_input.text.strip()
            if new_text:
                self.messages[index]["content"] = new_text
                self.messages[index]["metadata"]["edited"] = True
                self.update_chat_area()
                self.save_messages()
            self.edit_popup.dismiss()

        save_button.bind(on_release=save_edit)
        content.add_widget(save_button)

        self.edit_popup = Popup(title="Редактировать сообщение", content=content, size_hint=(0.8, 0.5))
        self.edit_popup.open()

    def replace_photo(self, index):
        self.popup.dismiss()
        self.replace_index = index
        try:
            filechooser.open_file(
                title="Выберите новое изображение",
                filters=[("Images", "*.png;*.jpg;*.jpeg")],
                on_selection=self.on_replace_photo_selected
            )
        except Exception as e:
            print(f"Error opening file chooser for replacement: {e}")

    def on_replace_photo_selected(self, selection):
        try:
            if selection and len(selection) > 0:
                photo_path = selection[0]
                self.messages[self.replace_index]["content"] = photo_path
                self.messages[self.replace_index]["metadata"]["edited"] = True
                self.update_chat_area()
                self.save_messages()
                self.close_popup(None)  
        except Exception as e:
            print(f"Error processing replaced photo: {e}")

    def delete_message(self, index):
        self.popup.dismiss()
        content = BoxLayout(orientation='vertical')
        label = Label(text="Вы уверены, что хотите удалить это сообщение?")
        content.add_widget(label)

        yes_button = Button(text="Да")
        no_button = Button(text="Нет")

        def delete_and_close(instance):
            del self.messages[index]
            self.update_chat_area()
            self.save_messages()
            self.delete_popup.dismiss()

        yes_button.bind(on_release=delete_and_close)
        no_button.bind(on_release=self.close_popup)

        content.add_widget(yes_button)
        content.add_widget(no_button)

        self.delete_popup = Popup(title="Подтвердите удаление", content=content, size_hint=(0.8, 0.5))
        self.delete_popup.open()

    def clear_chat(self, instance):
        content = BoxLayout(orientation='vertical')
        label = Label(text="Вы уверены, что хотите удалить ВСЕ сообщения?\nЭто действие нельзя отменить!")
        content.add_widget(label)

        yes_button = Button(text="Да")
        no_button = Button(text="Нет")

        def clear_and_close(instance):
            self.messages.clear()
            self.update_chat_area()
            if os.path.exists("messages.txt"):
                os.remove("messages.txt")
            self.clear_popup.dismiss()

        yes_button.bind(on_release=clear_and_close)
        no_button.bind(on_release=self.close_popup)

        content.add_widget(yes_button)
        content.add_widget(no_button)

        self.clear_popup = Popup(title="Очистка чата", content=content, size_hint=(0.8, 0.5))
        self.clear_popup.open()

    def save_messages(self):
        try:
            with open("messages.txt", "w", encoding="utf-8") as f:
                for msg in self.messages:
                    f.write(f"{msg['type']}|{msg['content']}|{msg['metadata']['edited']}\n")
        except Exception as e:
            print(f"Error saving messages: {e}")

    def load_messages(self):
        try:
            if os.path.exists("messages.txt"):
                with open("messages.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split("|")
                        if len(parts) >= 3:
                            self.messages.append({
                                "type": parts[0],
                                "content": parts[1],
                                "metadata": {"edited": parts[2] == "True"}
                            })
                self.update_chat_area()
        except Exception as e:
            print(f"Error loading messages: {e}")

    def close_popup(self, instance):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()

    def open_drawing_popup(self, instance):
        self.drawing_popup = DrawingPopup()
        self.drawing_popup.open()


class ChatArea(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', size_hint_y=None, padding=10,
                                 spacing=5)  
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)

    def add_message(self, msg, index, context_menu_callback):
        if msg["type"] == "text":
            prefix = "[РЕД.] " if msg["metadata"]["edited"] else ""
            text = f"{prefix}{msg['content']}" 
            label = MessageLabel(text=text, size_hint_y=None, text_size=(self.width - 20, None), halign='left',
                                 valign='top', markup=True)  
        elif msg["type"] == "photo":
            try:
                pil_image = PILImage.open(msg["content"])
                pil_image.thumbnail((150, 150))
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                texture = CoreImage(io.BytesIO(img_byte_arr), ext='png').texture

                image = Image(texture=texture, size_hint_y=None, height=150)
                image.bind(on_touch_down=lambda instance, touch: self.on_message_touch(instance, touch, index,
                                                                                         context_menu_callback))
                self.layout.add_widget(image)
                return
            except Exception as e:
                label = Label(text=f"Ошибка загрузки изображения: {e}", size_hint_y=None, height=30)

        label.bind(on_touch_down=lambda instance, touch: self.on_message_touch(instance, touch, index,
                                                                                 context_menu_callback))
        self.layout.add_widget(label)

    def on_message_touch(self, instance, touch, index, context_menu_callback):
        if instance.collide_point(*touch.pos):
            if touch.is_double_tap:
                context_menu_callback(index)
                return True
        return False

    def clear_messages(self):
        self.layout.clear_widgets()


class MessageLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.valign = 'top'
        self.halign = 'left'
        self.text_size = (self.width - 20, None)  


class QwotaMessengerApp(App):
    def build(self):
        return QwotaMessenger()


if __name__ == '__main__':
    QwotaMessengerApp().run()
