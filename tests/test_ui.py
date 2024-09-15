from ..ui import UserInterface
from ..logic import ACTIONS_METHODS
from unittest.mock import patch, Mock
from PySide6.QtCore import QUrl, QByteArray
from .conftest import data_str_create, data_dict_create


def test_send_click(qtbot):
    ui = UserInterface()
    ui.send_click = Mock()
    ui.send_btn.click()
    ui.send_click.assert_called_once()


def test_get_request_data(qtbot):
    ui = UserInterface()
    ui.combo_box.setCurrentText(ACTIONS_METHODS.POST)
    url_str = "https://example.com/api"
    ui.url.setText(url_str)
    ui.body.setPlainText(data_str_create)
    expected_action_method = ACTIONS_METHODS.POST
    expected_url = QUrl(url_str)
    action_method, url, data = ui.get_request_data()
    data_str = str(data, "utf-8")
    assert action_method == expected_action_method
    assert url == expected_url
    for key in data_dict_create:
        assert key in data_str
    for value in data_dict_create.values():
        assert str(value) in data_str