from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QTabWidget,
    QListWidget,
    QLabel,
)
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QRestAccessManager,
)
from PySide6.QtCore import QUrl, QByteArray
import sys
import json
from functools import partial
from logic import ACTIONS_METHODS, get_status_message
from logic import handle_response, send_request


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 750, 750)

        main_vbox = QVBoxLayout(self)
        link_hbox = QHBoxLayout(self)
        results_hbox = QHBoxLayout(self)
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(list(ACTIONS_METHODS))
        self.url = QLineEdit(self)
        self.send_btn = QPushButton("Send", self)
        self.result = QTextEdit("{\n\n\n}", self)
        self.body = QTextEdit("{\n\n\n}")
        self.headers = QListWidget()
        self.params = QListWidget()
        self.status_label = QLabel(self)

        results_hbox.addWidget(self.result)
        link_hbox.addWidget(self.combo_box)
        link_hbox.addWidget(self.url)
        link_hbox.addWidget(self.send_btn)

        self.body.setAcceptRichText(False)
        self.setLayout(main_vbox)
        self.network_manager = QNetworkAccessManager()
        self.rest_manager = QRestAccessManager(self.network_manager)
        self.handle_response_update = partial(handle_response, callback=self.update_ui)
        self.network_manager.finished.connect(self.handle_response_update)
        self.send_btn.clicked.connect(self.send_click)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.params, "Params")
        self.tabs.addTab(self.headers, "Headers")
        self.tabs.addTab(self.body, "Body")
        self.status_label.setStyle(self.tabs.style())
        self.tabs.setCornerWidget(self.status_label)

        main_vbox.addLayout(link_hbox)
        main_vbox.addLayout(results_hbox)
        main_vbox.addWidget(self.tabs)

    def get_request_data(self):
        action_method = self.combo_box.currentText()
        json_dict = json.loads(
            self.body.toPlainText().encode("utf-8").decode("unicode_escape")
        )
        json_data = json.dumps(json_dict).encode("utf-8")

        data = QByteArray(json_data)
        url = QUrl(self.url.text())

        return action_method, url, data

    def send_click(self):
        send_request(self.rest_manager, *self.get_request_data())

    def update_ui(self, data, status_code, time):
        self.result.setPlainText(data)
        self.status_label.setText(f"{get_status_message(status_code)}, {time} ms")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()

    sys.exit(app.exec())
