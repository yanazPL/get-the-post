from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

class KeyValTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_row = 0
        self.setRowCount(1)
        self.setColumnCount(3)
        self.setItem(0, 1, QTableWidgetItem("Key"))
        self.setItem(0, 2, QTableWidgetItem("Value"))
        self.add_row_if_last(0,1)
        # self.add_row_if_last(0, 1)
        # self.add_row()
        # self.setCellWidget
        

        self.data = dict()
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setColumnWidth(0, 40)  # Fixed width of 100 pixels
        
        # Set resize mode for other columns
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # Expandable column 1
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)  # Expandable column 2

        def supress_double_click():
            # Prevent double-click from editing the cell
            pass

        self.itemDoubleClicked.connect(supress_double_click)
        self.cellChanged.connect(self.add_row_if_last)
    def add_row_if_last(self, row, column):
        if row == self.last_row:
            
            self.insertRow(self.last_row + 1)
            checkbox = QTableWidgetItem()
            checkbox.setCheckState(Qt.CheckState.Checked)
            key = QTableWidgetItem()
            key.setFlags(key.flags() | Qt.ItemIsEditable)
            val = QTableWidgetItem()
            val.setFlags(val.flags() | Qt.ItemIsEditable)
            self.setItem(self.last_row + 1, 0, checkbox)
            self.setItem(self.last_row + 1, 1, key)
            self.setItem(self.last_row + 1, 2, val)
            self.last_row += 1
    
    def get_data(self):
        pass

    def delete_row(row):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item:
                self.editItem(item)
        super().mousePressEvent(event)