from PySide6.QtWidgets import QCheckBox
from PySide6.QtGui import QDrag, QPixmap
from PySide6.QtCore import Qt, QMimeData

class DragCheck(QCheckBox):

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            drag.exec(Qt.MoveAction)