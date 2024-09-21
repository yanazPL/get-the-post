from unittest.mock import Mock
from key_val_table import KeyValTable, XBUTTON_COL, VALUE_COL, KEY_COL, CHECKBOX_COL
from PySide6.QtCore import Qt

Unchecked = Qt.CheckState.Unchecked
Checked = Qt.CheckState.Checked


def test_init(qtbot):
    table = KeyValTable()
    qtbot.add_widget(table)
    assert table.data == []
    assert table.rowCount() == 2
    assert table.columnCount() == 4
    assert table.horizontalHeader().isHidden()
    assert table.verticalHeader().isHidden()
    table.show()
    assert table.isVisible()


def fill_row_with_data(table, row, key, val, checkstate):
    table.item(row, KEY_COL).setText(key)
    table.item(row, VALUE_COL).setText(val)
    table.item(row, CHECKBOX_COL).setCheckState(checkstate)


def test_adding_deleting_rows(qtbot):
    table = KeyValTable()
    table.show()
    qtbot.add_widget(table)
    table.is_empty_row = Mock()
    table.is_empty_row.return_value = False
    table.add_row_if_last(1)
    table.add_row_if_last(2)
    table.add_row_if_last(3)
    table.add_row_if_last(4)
    assert table.rowCount() == 6
    table.cellWidget(4, XBUTTON_COL).click()
    table.cellWidget(3, XBUTTON_COL).click()
    table.cellWidget(2, XBUTTON_COL).click()
    table.cellWidget(1, XBUTTON_COL).click()
    assert table.rowCount() == 2


def test_first_xbutton_toggle(qtbot):
    table = KeyValTable()
    qtbot.add_widget(table)
    first_x_button = table.cellWidget(1, XBUTTON_COL)
    assert first_x_button.text() == ""
    table.is_empty_row = Mock()
    table.is_empty_row.return_value = False
    table.add_row_if_last(1)
    assert first_x_button.text() == "X"


def test_is_empty_row(qtbot):
    table = KeyValTable()
    qtbot.add_widget(table)
    table.item(1, VALUE_COL).setText("")
    table.item(1, KEY_COL).setText("")
    assert table.is_empty_row(1)
    table.item(1, VALUE_COL).setText("lorem")
    table.item(1, KEY_COL).setText("lorem")
    table.show()

    assert not table.is_empty_row(1)


def test_left_button_edit_item(qtbot):
    table = KeyValTable()
    qtbot.add_widget(table)
    table.show()
    qtbot.waitForWindowShown(table)
    val_item = table.item(1, VALUE_COL)
    key_item = table.item(1, KEY_COL)
    val_rect = table.visualItemRect(val_item)
    key_rect = table.visualItemRect(key_item)
    table.editItem = Mock()
    qtbot.mouseClick(table.viewport(), Qt.LeftButton, pos=val_rect.center())
    assert table.editItem.call_args.args == (val_item,)
    qtbot.mouseClick(table.viewport(), Qt.LeftButton, pos=key_rect.center())
    assert table.editItem.call_args.args == (key_item,)


def test_data(qtbot):
    table = KeyValTable()
    qtbot.add_widget(table)
    table.show()
    qtbot.waitForWindowShown(table)
    input_data = (
        ("k1", "v1", Checked),
        ("k1", "v1", Unchecked),
        ("", "empty_k", Checked),
        ("", "empty_k", Unchecked),
        ("k2", "v2", Checked),
        ("k2", "v2", Unchecked),
        ("k1", "v1", Checked),
        ("k2", "v2", Unchecked),
        ("empty_v", "", Checked),
        ("empty_v", "", Unchecked),
        ("k3", "v3", Unchecked),
        ("k3", "v3", Checked),
    )
    expected_result = [
        ("k1", "v1"),
        ("", "empty_k"),
        ("k2", "v2"),
        ("k1", "v1"),
        ("empty_v", ""),
        ("k3", "v3"),
    ]
    assert input_data[0] == ("k1", "v1", Checked)

    for row_data in input_data:
        fill_row_with_data(table, table.last_row, *row_data)

    table.refresh_data()
    assert table.data == expected_result


def test_check_uncheck(qtbot):
    table = KeyValTable()
    qtbot.add_widget(table)
    table.show()
    qtbot.waitForWindowShown(table)
    fill_row_with_data(table, 1, "k1", "v1", Checked)
    table.refresh_data()
    assert table.data == [("k1", "v1")]
    table.item(1, CHECKBOX_COL).setCheckState(Unchecked)
    table.refresh_data()
    assert table.data == []
