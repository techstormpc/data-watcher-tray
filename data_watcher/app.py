import os
import sys
from importlib import resources
from pathlib import Path
from threading import Thread
from typing import Callable, Union, Optional

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from data_watcher.log_dialog import LogDialog
from data_watcher.process import ProcessRunnable


class DataWatcher:
    """
    System tray application that provides the option to upload manually
     and run a background task
    """
    def __init__(self,
                 app_name: str,
                 icon_path: Optional[Union[str, Path]],
                 background_task: Callable[[], Thread] = None,
                 upload_callback: Callable[[], None] = None):
        """

        :param app_name: Application name (shows on window and tooltip)
        :param icon_path: Path to icon file, must exist, default icon if not provided
        :param background_task: Optional background task, see example
        :param upload_callback: Optional manual upload task, see example
        """
        if not icon_path:
            with resources.path("data_watcher", "icon-default.png") as icon:
                icon_path = icon

        if not Path(icon_path).exists():
            raise RuntimeError(f"Cannot find icon file {icon_path}")

        self.app_name = app_name
        self.icon_path = str(icon_path)
        self.upload_callback = upload_callback
        self.background_task = background_task

        if self.background_task:
            self.background_task = ProcessRunnable(target=background_task)
            self.background_task.start()

        os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        os.environ["QT_SCALE_FACTOR"] = "1"
        self.q_app = QApplication(sys.argv)
        self.q_app.setQuitOnLastWindowClosed(False)
        self._init_system_tray()

    def start(self):
        """ Run the application """
        return self.q_app.exec()

    def stop(self):
        """ Stop the application """
        if self.background_task:
            self.background_task.stop()
        QApplication.exit()

    def _init_system_tray(self):
        icon = QIcon(self.icon_path)
        tray = QSystemTrayIcon(self.q_app)
        tray.setIcon(icon)
        tray.setVisible(True)
        menu = QMenu()

        # Set up show log button
        self._log_dialog = LogDialog(app_name=self.app_name, app_icon=icon)
        log_action = menu.addAction("Log")
        log_action_font = log_action.font()
        log_action_font.setBold(True)
        log_action.setFont(log_action_font)
        log_action.triggered.connect(self._show_log_dialog)

        # Manual upload
        if self.upload_callback:
            menu.addAction("Manual Upload").triggered.connect(self.upload_callback)

        menu.addSeparator()

        # Exit
        menu.addAction("Exit").triggered.connect(self.stop)

        tray.setContextMenu(menu)
        tray.setToolTip(self.app_name)
        tray.activated.connect(self._tray_click_handler)

    def _tray_click_handler(self, value):
        if value == QSystemTrayIcon.ActivationReason.Trigger:
            self._show_log_dialog()

    def _show_log_dialog(self):
        self._log_dialog.exec()
