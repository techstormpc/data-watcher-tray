from threading import Thread
from typing import Callable

from PyQt6.QtCore import QRunnable, QThreadPool


class ProcessRunnable(QRunnable):
    def __init__(self, target: Callable[[], Thread]):
        QRunnable.__init__(self)
        self.target = target
        self.runnable = None

    def run(self):
        self.runnable = self.target()

    def start(self):
        QThreadPool.globalInstance().start(self)

    def stop(self):
        self.runnable.stop()
