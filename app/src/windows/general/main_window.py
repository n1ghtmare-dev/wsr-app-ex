from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel
from service.health_checker import HealthCheckerService
from windows.base.main_window_ui import Ui_MainWindow
from windows.utils.worker_thread import WorkerThread



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.service = HealthCheckerService()
        self.btn_full_test.clicked.connect(self.start_all)
        self.btn_open_config.clicked.connect(self.open_page_config)
        self.btn_open_main.clicked.connect(self.open_page_main)
        self.btn_save_config.clicked.connect(self.save_config)
        self.btn_choice_testfile.clicked.connect(self.edit_testfile)
        self.threads = []

    def start_all(self) -> None:
        self.run_thread(self.service.check_internet)

    def add_action(self, text) -> None:
        label = QLabel(text)
        self.verticalLayout.insertWidget(0, label)

    def run_thread(self, func, *args, **kwargs) -> None:
        thread = WorkerThread(func, *args, **kwargs)
        thread.finished.connect(lambda: self.threads.remove(thread))
        thread.result_signal.connect(self.add_action)
        self.threads.append(thread)
        thread.start()

    def open_page_main(self) -> None:
        self.stackedWidget.setCurrentWidget(self.page_main)

    def open_page_config(self) -> None:
        self.stackedWidget.setCurrentWidget(self.page_config)

    def save_config(self) -> None:
        host = self.linec_host.text()
        test_file = self.linec_file.text()

        self.service.hostname = host

    def edit_testfile(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(caption="Выберите файл")

        if file_path:
            print(file_path)
            self.service.test_file_path = file_path
            self.linec_file.setText(file_path)
            self.add_action(f'Тестовый файл обновлен: {file_path}')


def start_app():
    import sys 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())