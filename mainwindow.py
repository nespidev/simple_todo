from PySide6.QtWidgets import QMainWindow, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QCheckBox, QScrollArea
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from pathlib import Path
import json
import os
import sys
import resource_rc

# mainwindow.py - Defines the MainWindow class for the Simple Todo application.
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Simple Todo")
        self.setWindowIcon(QIcon(":/start.png"))
        self.resize(400,550)

        # Determine the path to the script's directory
        script_dir = Path(os.path.dirname(sys.argv[0]))

        # Use the script directory to find the bundled data
        self.data_path = script_dir

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
            self.task_check_box_list.append(task_check_box)

        self.task_layout.setAlignment(Qt.AlignTop)

        for task_check_box in self.task_check_box_list:
            task_check_box.toggled.connect(self.check_box_clicked)
            if task_check_box.isChecked():
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
            self.task_layout.addWidget(new_task_check_box)
            task_item = [text, False]
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


    def save_tasks(self):
        # Use the data_path to create the full path to todo.json
        todo_path = self.data_path / "todo.json"

        with open(todo_path, 'w') as file:
            json.dump(self.task_list, file, indent=4)
        print(f"Saved tasks: {self.task_list}")

    def load_tasks(self):
        try:
            # Use the data_path to create the full path to todo.json
            todo_path = self.data_path / "todo.json"

            with open(todo_path, 'r') as file:
                self.task_list = json.load(file)
        except FileNotFoundError:
            self.task_list = []

        print(f"Loaded tasks: {self.task_list}")