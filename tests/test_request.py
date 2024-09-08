import pytest
from ..ui import UserInterface


data_str = '''{
    "id": 1,
    "title": "foo",
    "body": "bar",
    "userId": 1
}'''

@pytest.mark.parametrize("data_str", [data_str])
def test_post(qtbot, data_str):
    ui = UserInterface()
    qtbot.add_widget(ui)
    ui.combo_box.setCurrentText("POST")
    ui.url.setText("https://jsonplaceholder.typicode.com/posts")
    ui.body.setPlainText(data_str)
    result_before = ui.result.toPlainText()
    ui.send_btn.click()
    qtbot.wait(1000) #TODO qtbot.waitSignal(ui.rest_logic.network_manager.finished) doesnt wait for callback
    assert ui.result.toPlainText() != result_before


def test_get(qtbot):
    ui = UserInterface()
    qtbot.add_widget(ui)
    ui.show()
    ui.combo_box.setCurrentText("GET")
    ui.url.setText("https://jsonplaceholder.typicode.com/posts")
    result_before = ui.result.toPlainText()
    ui.send_btn.click()
    qtbot.wait(1000) #TODO qtbot.waitSignal(ui.rest_logic.network_manager.finished) doesnt wait for callback
    assert ui.result.toPlainText() != result_before

