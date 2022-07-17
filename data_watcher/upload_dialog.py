from pathlib import Path
from typing import Callable

from PyQt6.QtWidgets import QWidget, QFileDialog


class FileUploadDialog(QWidget):
    """
    File Upload Dialog, useful in upload callback
    """
    def __init__(self,
                 app_name: str,
                 on_select: Callable[[Path], None],
                 default_directory: str = '',
                 allowed_files_filter: str = 'All Files(*)'):
        super().__init__()
        self.setWindowTitle(f"{app_name} - Manual Upload")

        dialog = QFileDialog()
        file_name, _ = dialog.getOpenFileName(self,
                                              caption="Open Data File",
                                              directory=default_directory,
                                              filter=allowed_files_filter)
        if file_name and file_name != '':
            on_select(Path(file_name))
