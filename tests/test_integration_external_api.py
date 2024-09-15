import pytest
from ..ui import UserInterface
from ..logic import ACTIONS_METHODS
from .conftest import data_str_create, data_str_update, NON_EXISTING_ID, EXISTING_ID


@pytest.mark.exapi()
@pytest.mark.parametrize("data_str", [data_str_create])
def test_post(qtbot, data_str):
    ui = UserInterface()
    qtbot.add_widget(ui)
    ui.combo_box.setCurrentText(ACTIONS_METHODS.POST)
    ui.url.setText("https://jsonplaceholder.typicode.com/posts")
    ui.body.setPlainText(data_str)
    result_before = ui.result.toPlainText()
    ui.send_btn.click()
    qtbot.wait(1000)
    # TODO qtbot.waitSignal(ui.rest_logic.network_manager.finished) doesnt wait for callback
    assert ui.result.toPlainText() != result_before


@pytest.mark.exapi()
def test_get_list(qtbot):
    ui = UserInterface()
    qtbot.add_widget(ui)
    ui.show()
    ui.combo_box.setCurrentText(ACTIONS_METHODS.GET)
    ui.url.setText("https://jsonplaceholder.typicode.com/posts")
    result_before = ui.result.toPlainText()
    ui.send_btn.click()
    qtbot.wait(1000)
    # TODO qtbot.waitSignal(ui.rest_logic.network_manager.finished) doesnt wait for callback
    assert ui.result.toPlainText() != result_before


@pytest.mark.exapi()
def test_get_one(qtbot):
    ui = UserInterface()
    qtbot.add_widget(ui)
    ui.show()
    ui.combo_box.setCurrentText(ACTIONS_METHODS.GET)
    ui.url.setText(f"https://jsonplaceholder.typicode.com/posts/{EXISTING_ID}")
    result_before = ui.result.toPlainText()
    ui.send_btn.click()
    qtbot.wait(1000)
    # TODO qtbot.waitSignal(ui.rest_logic.network_manager.finished) doesnt wait for callback
    assert ui.result.toPlainText() != result_before


@pytest.mark.exapi()
def test_patch(qtbot):
    ui = UserInterface()
    qtbot.add_widget(ui)
    ui.show()
    ui.combo_box.setCurrentText(ACTIONS_METHODS.PATCH)
    ui.url.setText(f"https://jsonplaceholder.typicode.com/posts/{EXISTING_ID}")
    data_str = '{"title": "Test title"}'
    ui.body.setPlainText(data_str)
    result_before = ui.result.toPlainText()
    ui.send_btn.click()
    qtbot.wait(1000)
    # TODO qtbot.waitSignal(ui.rest_logic.network_manager.finished) doesnt wait for callback
    assert ui.result.toPlainText() != result_before


@pytest.mark.exapi()
def test_delete(qtbot):
    ui = UserInterface()
    qtbot.add_widget(ui)
    ui.show()
    ui.combo_box.setCurrentText(ACTIONS_METHODS.DELETE)
    ui.url.setText(f"https://jsonplaceholder.typicode.com/posts/{EXISTING_ID}")
    result_before = ui.result.toPlainText()
    ui.send_btn.click()
    qtbot.wait(1000)
    # TODO qtbot.waitSignal(ui.rest_logic.network_manager.finished) doesnt wait for callback
    assert ui.result.toPlainText() != result_before


@pytest.mark.exapi()
@pytest.mark.parametrize("data_str", [data_str_create, data_str_update])
def test_put(qtbot, data_str):
    ui = UserInterface()
    qtbot.add_widget(ui)
    ui.show()
    ui.combo_box.setCurrentText(ACTIONS_METHODS.PUT)
    ui.url.setText(f"https://jsonplaceholder.typicode.com/posts/{EXISTING_ID}")
    ui.body.setPlainText(data_str)
    result_before = ui.result.toPlainText()
    ui.send_btn.click()
    qtbot.wait(1000)
    # TODO qtbot.waitSignal(ui.rest_logic.network_manager.finished) doesnt wait for callback
    assert ui.result.toPlainText() != result_before
