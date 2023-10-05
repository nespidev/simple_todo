from PySide6.QtWidgets import QMainWindow, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QDateEdit, QCheckBox, QGroupBox, QSpacerItem
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
from pathlib import Path
import datetime


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Simple Todo")
        self.setWindowIcon(QIcon("pyqt/exp/programa_todo/start.png"))
        central_widget = QWidget()
        todo_box = QGroupBox("To do:")

        self.task_list = []
        self.task_check_box_list = []
        self.load_tasks()
        
        ###### ESTO ES UN TEST ##########
        #self.task_list.append("ejemplo")

        self.save_tasks()
        layout = QVBoxLayout()

        new_task_layout = QHBoxLayout()
        new_task_label = QLabel("New task:")
        self.new_task_line_edit = QLineEdit()
        add_task_button = QPushButton("Add")
        add_task_button.clicked.connect(self.add_task_button_clicked)

        new_task_layout.addWidget(new_task_label)
        new_task_layout.addWidget(self.new_task_line_edit)
        new_task_layout.addWidget(add_task_button)
        
        self.task_layout = QVBoxLayout()
        for task in self.task_list:
            task_check_box = QCheckBox(task)
            self.task_layout.addWidget(task_check_box)
            # Append the task_check_box to the list
            self.task_check_box_list.append(task_check_box)

        for task_check_box in self.task_check_box_list:
            task_check_box.toggled.connect(self.check_box_clicked)

        done_button_layout = QHBoxLayout()
        done_button = QPushButton("Done")
        done_button.clicked.connect(self.done_button_clicked)
        done_button_layout.addWidget(done_button)


        layout.addLayout(new_task_layout)
        todo_box.setLayout(self.task_layout)
        layout.addWidget(todo_box)
        layout.addLayout(done_button_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)        

    def add_task_button_clicked(self):
        text = self.new_task_line_edit.text()
        if text != "":
            new_task_check_box = QCheckBox(text)
            self.task_layout.addWidget(new_task_check_box)
            self.task_list.append(text)
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


    def done_button_clicked(self):
        print(str(self.task_list))
        print(str(self.task_check_box_list))
        check_boxes_to_remove = []
        for check_box in self.task_check_box_list:
            if check_box.isChecked():
                check_boxes_to_remove.append(check_box)

        for check_box in check_boxes_to_remove:
            self.task_list.remove(check_box.text())
            self.task_check_box_list.remove(check_box)
            check_box.deleteLater()
            self.task_layout.removeWidget(check_box)
        
        self.save_tasks()

    # Save task in a file
    def save_tasks(self):
        with open(Path(__file__).with_name("todo.txt"), 'w') as file:
            for task in self.task_list:
                file.write(task + '\n')
        print(f"Saved tasks:{self.task_list}")

    # Load tasks from a file
    def load_tasks(self):
        with open(Path(__file__).with_name("todo.txt"), 'r') as file:
            self.task_list = file.read().splitlines()
        print(f"Loaded tasks:{self.task_list}")



    def delete_checked_checkboxes_old(self):
        # Iterate over the checkboxes and remove checked ones
        checkboxes_to_remove = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                checkboxes_to_remove.append(checkbox)

        for checkbox in checkboxes_to_remove:
            self.layout.removeWidget(checkbox)
            checkbox.deleteLater()
            self.checkboxes.remove(checkbox)

 