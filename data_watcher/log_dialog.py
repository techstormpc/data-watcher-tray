import logging
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QPlainTextEdit, QVBoxLayout

logger = logging.getLogger()


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class LogDialog(QDialog, QPlainTextEdit):
    def __init__(self, app_name: str, app_icon: QIcon):
        super().__init__(parent=None)

        self.setWindowTitle(f"{app_name} - Log")
        self.setWindowIcon(app_icon)

        log_text_box = QTextEditLogger(self)
        log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                       "%Y-%m-%d %H:%M:%S")
        log_text_box.setFormatter(log_format)
        logger.addHandler(log_text_box)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.setLevel(logging.INFO)

        layout = QVBoxLayout()
        self.resize(750, 500)
        layout.addWidget(log_text_box.widget)
        self.setLayout(layout)
