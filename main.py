import sys
from PyQt6.QtWidgets import QApplication
from gui.window import ZenoWindow

app = QApplication(sys.argv)

window = ZenoWindow()
window.show()

sys.exit(app.exec())