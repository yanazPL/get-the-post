from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QPushButton

CHECKBOX_COL = 0
KEY_COL = 1
VALUE_COL = 2
XBUTTON_COL = 3
CHECKBOX_WIDTH = 40
XBUTTON_WIDTH = 40


class KeyValTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.last_row = 0
        self.setRowCount(1)
        self.setColumnCount(4)
        self.left_corner = QTableWidgetItem()
        self.right_corner = QTableWidgetItem()
        self.key_header = QTableWidgetItem("Key")
        self.val_header = QTableWidgetItem("Value")

        self.setItem(0, KEY_COL, self.key_header)
        self.setItem(0, VALUE_COL, self.val_header)
        self.setItem(0, 0, self.left_corner)
        self.setItem(0, 3, self.right_corner)
        self.key_header.setFlags(
            self.key_header.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
        )
        self.val_header.setFlags(
            self.val_header.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
        )
        self.left_corner.setFlags(
            self.left_corner.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
        )
        self.right_corner.setFlags(
            self.right_corner.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
        )
        self.add_row_if_last(0)

        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setColumnWidth(CHECKBOX_COL, CHECKBOX_WIDTH)
        self.setColumnWidth(XBUTTON_COL, XBUTTON_WIDTH)

        self.horizontalHeader().setSectionResizeMode(
            KEY_COL, QHeaderView.Stretch
        )  # Expandable column 1
        self.horizontalHeader().setSectionResizeMode(
            VALUE_COL, QHeaderView.Stretch
        )  # Expandable column 2

        def supress_double_click():
            # Prevent double-click from editing the cell
            pass

        self.itemDoubleClicked.connect(supress_double_click)
        self.cellChanged.connect(self.add_row_if_last)

    def is_empty_row(self, row):
        return (
            not self.item(row, KEY_COL).text() and not self.item(row, VALUE_COL).text()
        )

    def add_row_if_last(self, row=None):
        if row == self.last_row and not self.is_empty_row(row):
            self.insertRow(self.last_row + 1)
            checkbox = QTableWidgetItem()
            checkbox.setCheckState(Qt.CheckState.Checked)
            checkbox.setFlags(
                checkbox.flags() & ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
            )
            key = QTableWidgetItem()
            key.setFlags((key.flags() & ~Qt.ItemIsSelectable) | Qt.ItemIsEditable)
            val = QTableWidgetItem()
            val.setFlags(val.flags() | Qt.ItemIsEditable & ~Qt.ItemIsSelectable)
            self.setItem(self.last_row + 1, CHECKBOX_COL, checkbox)
            self.setItem(self.last_row + 1, KEY_COL, key)
            self.setItem(self.last_row + 1, VALUE_COL, val)

            self.last_row += 1
            # Below uses new last row (incrementd)
            self.add_x_button(self.last_row)
            self.update_first_x_button()

    def refresh_data(self):
        self.data.clear()
        for row in range(1, self.rowCount()):
            checkbox = self.item(row, CHECKBOX_COL)
            key = self.item(row, KEY_COL).text()
            val = self.item(row, VALUE_COL).text()
            if checkbox.checkState() == Qt.Checked and (key or val):
                self.data.append((key, val))

    def add_x_button(self, row, col=XBUTTON_COL):
        button = QPushButton("X")
        item_in_row = self.item(
            row, 2
        )  # Could be any other non widget item in button's row
        button.clicked.connect(lambda: self.delete_row(item_in_row))
        self.setCellWidget(row, col, button)

    def delete_row(self, item_in_row):
        """item (not row) passed because row can change after deletion"""
        if not self.rowCount() > 2:
            return
        self.removeRow(item_in_row.row())
        self.last_row -= 1
        self.update_first_x_button()

    def update_first_x_button(self):
        xbutton = self.cellWidget(1, XBUTTON_COL)
        if self.rowCount() == 2:
            xbutton.setText("")
        if self.rowCount() == 3:
            xbutton.setText("X")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if (
                item
                and item.column() != CHECKBOX_COL
                and item
                not in (
                    self.key_header,
                    self.val_header,
                    self.right_corner,
                    self.left_corner,
                )
            ):
                self.editItem(item)
                print("edit")
        super().mousePressEvent(event)
