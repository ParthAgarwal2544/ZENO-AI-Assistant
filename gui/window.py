from ai.assistant import ask_zeno
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QApplication
)


class ZenoWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ZENO")
        self.setGeometry(100, 100, 1000, 700)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }

            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #333;
                font-size: 14px;
                padding: 8px;
            }

            QLineEdit {
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444;
                padding: 8px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #005ea6;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Talk to Zeno...")
        self.input_box.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        self.stop_button = QPushButton("Stop Speaking")
        self.stop_button.clicked.connect(self.stop_speaking)

        layout.addWidget(self.chat_area)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)
        layout.addWidget(self.stop_button)

        central_widget.setLayout(layout)

        self.chat_area.append("🤖 Zeno: Online and ready.")

    def send_message(self):
        message = self.input_box.text().strip()

        if not message:
            return

        self.chat_area.append(f"🧑 You: {message}")
        self.input_box.clear()

        self.chat_area.append("🤖 Zeno: Thinking...")
        QApplication.processEvents()

        try:
            response = ask_zeno(message)

            text = self.chat_area.toPlainText().split("\n")

            if text and text[-1] == "🤖 Zeno: Thinking...":
                text.pop()

            self.chat_area.setPlainText("\n".join(text))

            self.chat_area.append(f"🤖 Zeno: {response}")

        except Exception as e:
            self.chat_area.append(f"❌ Error: {str(e)}")

    def stop_speaking(self):
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.stop()

            self.chat_area.append("🤖 Zeno: Speech stopped.")

        except Exception as e:
            self.chat_area.append(f"❌ Error: {str(e)}")


# Backward compatibility alias
JarvisWindow = ZenoWindow