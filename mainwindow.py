from PySide6.QtWidgets import QMainWindow, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QDateEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import QDate
from pathlib import Path
import datetime


#IGNORE
class MainWindow2(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Guardar Texto")
        self.setWindowIcon(QIcon("pyqt/exp/guardar_texto_2/start.png"))
        
        central_widget = QWidget()
        label_nombre = QLabel("Nombre:")
        self.line_edit_nombre = QLineEdit()
        label_apellido = QLabel("Apellido:")
        self.line_edit_apellido = QLineEdit()
        label_fecha = QLabel("Fecha:")
        self.date_edit = QDateEdit()

        current_date = datetime.datetime.now()
        self.date_edit.setDisplayFormat("dd/MM/yy")
        self.date_edit.setDate(QDate(current_date.year,current_date.month,current_date.day))
        
        self.button_guardar = QPushButton("Guardar")
        self.button_guardar.clicked.connect(self.guardar_archivo)

        layout = QVBoxLayout()
        layout.addWidget(label_apellido)
        layout.addWidget(self.line_edit_apellido)
        layout.addWidget(label_nombre)
        layout.addWidget(self.line_edit_nombre)
        layout.addWidget(label_fecha)
        layout.addWidget(self.date_edit)
  
        layout.addWidget(self.button_guardar)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)



    def guardar_archivo(self):
        if self.verificar_line_edit():
            nombre = self.line_edit_nombre.text()
            apellido = self.line_edit_apellido.text().upper()

            date = self.date_edit.date()
            date_str = date.toString("dd-MM-yyyy")
            date_str2= date.toString("dd/MM/yyyy")
            
            nombre_archivo = (date_str+" "+nombre+" "+apellido).upper()+".txt"

            p = Path(__file__).with_name(nombre_archivo)
            archivo = open(p,"w+")
            texto = "Fecha: "+date_str2+"\nNombre: "+nombre+"\nApellido: "+apellido
            
            archivo.write(texto)
            archivo.close()
            
            self.line_edit_apellido.clear()
            self.line_edit_nombre.clear()

    def verificar_line_edit(self):
        if self.line_edit_nombre.text() == "" and self.line_edit_apellido.text() =="":
            print("Ingresa un apellido y un nombre para continuar.")
            return False
        elif self.line_edit_nombre.text() == "":
            print("Ingresa un nombre para continuar.")
            return False
        elif self.line_edit_apellido.text() == "":
            print("Ingresa un apellido para continuar")
            return False
        else:
            return True

        
    def quit(self):
        self.app.quit()




class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("To-do")
        self.setWindowIcon(QIcon("pyqt/exp/programa_todo/start.png"))

        self.task_list = []
        self.load_tasks()
        print(f"Loaded tasks:{self.task_list}")
        self.task_list.append("\nejemplo")
        self.save_tasks()
        print(f"Saved tasks:{self.task_list}")


    # Save task in a file
    def save_tasks(self):
        with open(Path(__file__).with_name("todo.txt"), 'w') as file:
            for task in self.task_list:
                file.write(task + '\n')

    # Load tasks from a file
    def load_tasks(self):
        with open(Path(__file__).with_name("todo.txt"), 'r') as file:
            self.task_list = file.read().splitlines()

    def test_functino(self):
        pass