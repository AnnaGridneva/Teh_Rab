import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont

class Game(QWidget):
    def __init__(self): 
        super().__init__()  
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Игра: Бочёнки")
        self.setStyleSheet("background-color: #f0f0f0;")  # Цвет фона
        self.setGeometry(100, 100, 400, 200)  # Размер окна
        
        # Фиксированные суммы
        self.amounts = [1, 10, 15, 1000, 10000, 25000, 50000, 75000, 100000, 150000, 250000, 300000, 1000000, 2000000, 3000000]
        random.shuffle(self.amounts)
        
        # Создание кнопок
        self.buttons = []
        grid = QGridLayout()  # Используем Grid Layout для кнопок

        for i in range(15):
            btn = QPushButton(f'БОЧЁНОК {i + 1}', self)
            btn.clicked.connect(lambda checked, idx=i: self.button_clicked(idx))
            self.buttons.append(btn)
            row = i // 5
            col = i % 5
            grid.addWidget(btn, row, col)  # Распределяем кнопки по сетке
        
        # Создание списка оставшихся сумм
        self.label = QLabel(self)
        self.label.setFont(QFont("Arial", 12))
        self.label.setStyleSheet("color: #333;")  # Цвет текста
        self.update_label()
        
        grid.addWidget(self.label, 3, 0, 1, 5)  # Добавляем label в сетку
        self.setLayout(grid)

    def button_clicked(self, index):
        btn = self.buttons[index]
        amount = self.amounts[index]
        self.amounts[index] = None  # Удаляем сумму из списка
        self.update_label()
        
        # Красим кнопку в красный и делаем её неактивной
        btn.setStyleSheet("background-color: red; color: white;")
        btn.setEnabled(False)
        
        # Показываем сообщение
        QMessageBox.information(self, "Результат", f"Вы проиграли {amount} рублей")
        
        # Проверка окончания игры
        if all(a is None for a in self.amounts):
            remaining = [a for a in self.amounts if a is not None]
            if remaining:
                QMessageBox.information(self, "Вы выиграли!", f"Вы выиграли {remaining[0]} рублей")
            self.close()

    def update_label(self):
        remaining_amounts = [str(a) for a in self.amounts if a is not None]
        self.label.setText("Оставшиеся суммы:\n" + ',  '.join(remaining_amounts))       
      
if __name__ == "__main__":  
    app = QApplication(sys.argv)
    game = Game()
    game.show()
    sys.exit(app.exec_())

