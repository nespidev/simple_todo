from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QCheckBox, QGroupBox, QSizePolicy, QScrollArea
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
import json
from pathlib import Path

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Simple Todo")
        self.setWindowIcon(QIcon("pyqt/exp/simple_todo/start.png"))
        self.resize(400,550)

        central_widget = QWidget()
        self.scroll_area = QScrollArea()  # Create a scroll area
        self.todo_widget = QWidget()

        self.task_list = []
        self.task_check_box_list = []
        self.load_tasks()
        
        layout = QVBoxLayout()

        new_task_layout = QHBoxLayout()
        new_task_label = QLabel("New task:")
        self.new_task_line_edit = QLineEdit()
        self.add_task_button = QPushButton("Add")
        self.add_task_button.clicked.connect(self.add_task_button_clicked)
        self.new_task_line_edit.returnPressed.connect(self.add_task_button.click)

        new_task_layout.addWidget(new_task_label)
        new_task_layout.addWidget(self.new_task_line_edit)
        new_task_layout.addWidget(self.add_task_button)
        
        self.task_layout = QVBoxLayout()
        for task, checked in self.task_list:
            task_check_box = QCheckBox(task)
            task_check_box.setChecked(checked)
            self.task_layout.addWidget(task_check_box)
            task_check_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)  # Set minimum height for checkboxes
            self.task_check_box_list.append(task_check_box)

        self.task_layout.setAlignment(Qt.AlignTop)

        for task_check_box in self.task_check_box_list:
            task_check_box.toggled.connect(self.check_box_clicked)
            if task_check_box.isChecked():
                # Set font strikeout for initially checked checkboxes
                font = task_check_box.font()
                font.setStrikeOut(True)
                task_check_box.setFont(font)

        done_button_layout = QHBoxLayout()
        done_button = QPushButton("Done")
        done_button.clicked.connect(self.done_button_clicked)
        done_button_layout.addWidget(done_button)

        self.todo_widget.setLayout(self.task_layout)  # Set the group box layout

        # Add the group box to the scroll area
        self.scroll_area.setWidget(self.todo_widget)
        self.scroll_area.setWidgetResizable(True)  # Allow the widget to resize

        layout.addLayout(new_task_layout)
        layout.addWidget(self.scroll_area)  # Add the scroll area to the layout
        layout.addLayout(done_button_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)  

    def add_task_button_clicked(self):
        text = self.new_task_line_edit.text()
        if text != "":
            new_task_check_box = QCheckBox(text)
            new_task_check_box.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)  # Set minimum height for checkboxes
            self.task_layout.addWidget(new_task_check_box)
            task_item = [text, False]  # Add the task as a list [text, checked)]
            self.task_list.append(task_item)
            self.task_check_box_list.append(new_task_check_box)
            new_task_check_box.toggled.connect(self.check_box_clicked)
            self.new_task_line_edit.clear()
            self.save_tasks()

    def check_box_clicked(self, checked):
        task_check_box = self.sender()  # Get the checkbox that emitted the signal
        font = task_check_box.font()

        if checked:
            print("is checked")
            font.setStrikeOut(True)
            task_check_box.setFont(font)
        else:
            print("not checked")
            font.setStrikeOut(False)
            task_check_box.setFont(font)

        # Update the task_list with the checkbox state
        for task_item in self.task_list:
            if task_item[0] == task_check_box.text():
                task_item[1] = checked  # Update the checkbox state in the existing list

        self.save_tasks()



    def done_button_clicked(self):
        print(str(self.task_list))

        items_to_remove = []
        
        for i, check_box in enumerate(self.task_check_box_list):
            if check_box.isChecked():
                items_to_remove.append(i)
        
        # Remove items from the end of the list to avoid index shifting issues
        items_to_remove.sort(reverse=True)
        for i in items_to_remove:
            removed_item = self.task_list.pop(i)
            self.task_check_box_list[i].deleteLater()
            self.task_check_box_list.pop(i)
        
        self.save_tasks()

    # Save tasks to a JSON file
    def save_tasks(self):
        with open(Path(__file__).with_name("todo.json"), 'w') as file:
            json.dump(self.task_list, file, indent=4)
        print(f"Saved tasks:{self.task_list}")

    # Load tasks from a JSON file
    def load_tasks(self):
        try:
            with open(Path(__file__).with_name("todo.json"), 'r') as file:
                self.task_list = json.load(file)
        except FileNotFoundError:
            self.task_list = []

        print(f"Loaded tasks:{self.task_list}")
