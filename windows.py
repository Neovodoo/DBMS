from PyQt5 import QtWidgets
from PyQt5 import Qt
from QT_DESIGN.main_window import Ui_Widget as main_Ui_Widget
from QT_DESIGN.edit_window import Ui_Widget as edit_Ui_Widget
from storage import Storage


class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.columns = ['id', 'name', 'was present', 'group', 'mark']
        self.ui = main_Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle('Student DBMS')
        self.storage = Storage()
        self.init_ui()

    def init_ui(self):
        self.ui.new_db_btn.clicked.connect(self.new_db_handler)
        self.ui.open_db_btn.clicked.connect(self.open_db_handler)
        self.ui.del_db_btn.clicked.connect(self.del_db_handler)
        self.ui.clear_db_btn.clicked.connect(self.clear_db_handler)
        self.ui.save_db_btn.clicked.connect(self.save_db_handler)

        self.ui.new_rec_btn.clicked.connect(self.new_rec_handler)
        self.ui.edit_rec_btn.clicked.connect(self.edit_rec_handler)
        self.ui.del_search_action_combo.addItems(['delete', 'search'])
        self.ui.del_search_selector_combo.addItems(self.columns)
        self.ui.del_search_ok_btn.clicked.connect(self.del_search_ok_btn_handler)

        self.ui.backup_store_btn.clicked.connect(self.backup_store_handler)
        self.ui.backup_restore_btn.clicked.connect(self.backup_restore_handler)

        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setShowGrid(True)
        self.ui.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.ui.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.tableWidget.setHorizontalHeaderLabels(self.columns)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)

    def new_db_handler(self):
        file, ok = QtWidgets.QInputDialog.getText(self, 'New db', 'name')
        if ok:
            if self.storage.new_db(db_name=file):
                self.ui.info_label.setText(f'{file} created')
            else:
                self.ui.info_label.setText('Database creatiion error')
        self.update_ui(self.storage.get_records())

    def open_db_handler(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open db')
        if self.storage.open_db(db_name=file):
            self.ui.info_label.setText(f'Open: {file}')
        self.update_ui(self.storage.get_records())

    def del_db_handler(self):
        if self.storage.delete_db():
            self.ui.info_label.setText(f'Delete: {self.storage.db_file}')
        else:
            self.ui.info_label.setText('Error deleting db')
        self.update_ui(self.storage.get_records())

    def clear_db_handler(self):
        if self.storage.clear_db():
            self.ui.info_label.setText(f'Clear: {self.storage.db_file}')
        else:
            self.ui.info_label.setText('Error clearing db')
        self.update_ui(self.storage.get_records())

    def save_db_handler(self):
        file, ok = QtWidgets.QInputDialog.getText(self, 'Save', 'name')
        if not ok:
            return
        if self.storage.copy_db(name=file):
            self.ui.info_label.setText('Saved ok')
        else:
            self.ui.info_label.setText('Error while saving db')
        self.update_ui(self.storage.get_records())

    def new_rec_handler(self):
        if not self.storage.new_record():
            self.ui.info_label.setText('Database not found')
        self.update_ui(self.storage.get_records())

    def edit_rec_handler(self):
        row = self.ui.tableWidget.currentRow()
        if row < 0:
            return
        data = []
        for i in range(5):
            data.append(self.ui.tableWidget.item(row, i).text())
        EditWindow(self,
                   callback=self.edit_rec_callback,
                   id_=data[0],
                   name=data[1],
                   was_present=data[2],
                   group=data[3],
                   mark=data[4]).show()

    def edit_rec_callback(self, id_, name, was_present, group, mark):
        if not self.storage.edit_record(i=id_, values=[name, was_present, group, mark]):
            self.ui.info_label.setText('Success!')
        else:
            self.update_ui(self.storage.get_records())

    def del_search_ok_btn_handler(self):
        action = self.ui.del_search_action_combo.currentText()
        field = self.ui.del_search_selector_combo.currentText()
        value = self.ui.del_search_value_line.text()
        if not self.storage.db_file:
            return
        if action == 'delete':
            self.storage.delete_record(field=field, value=value)
            self.update_ui(self.storage.get_records())
        elif action == 'search':
            if not value:
                self.update_ui(self.storage.get_records())
            else:
                records = self.storage.search_record(field=field, value=value)
                self.update_ui(records)

    def backup_store_handler(self):
        file, ok = QtWidgets.QInputDialog.getText(self, 'Create backup', 'file')
        if not ok:
            return
        if self.storage.copy_db(name=file):
            self.ui.info_label.setText('Backup successfully created')
        self.update_ui(self.storage.get_records())

    def backup_restore_handler(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Restore backup')
        if self.storage.open_db(db_name=file):
            self.ui.info_label.setText(f'Backup successfully restored')
        self.update_ui(self.storage.get_records())

    def update_ui(self, records):
        self.ui.tableWidget.setRowCount(0)
        for k, rec in enumerate(records):
            self.ui.tableWidget.insertRow(k)
            self.ui.tableWidget.setItem(k, 0, QtWidgets.QTableWidgetItem(str(rec.id)))
            self.ui.tableWidget.setItem(k, 1, QtWidgets.QTableWidgetItem(rec.name))
            self.ui.tableWidget.setItem(k, 2, QtWidgets.QTableWidgetItem(str(rec.was_present)))
            self.ui.tableWidget.setItem(k, 3, QtWidgets.QTableWidgetItem(str(rec.group)))
            self.ui.tableWidget.setItem(k, 4, QtWidgets.QTableWidgetItem(str(rec.mark)))


class EditWindow(QtWidgets.QMainWindow):
    def __init__(self, root, callback, id_, name, was_present, group, mark):
        super(EditWindow, self).__init__(root)
        self.callback = callback
        self.ui = edit_Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle('Edit record')
        self.ui.was_present_combo.addItems(['true', 'false'])
        self.ui.ok_btn.clicked.connect(self.ok_btn)
        self.ui.id_label.setText(id_)
        self.ui.name_line.setText(name)
        self.ui.was_present_combo.setCurrentIndex(0 if was_present.lower() == 'true' else 1)
        self.ui.group_line.setText(group)
        self.ui.mark_line.setText(mark)

    def ok_btn(self):
        id_ = self.ui.id_label.text()
        name = self.ui.name_line.text()
        was_present = self.ui.was_present_combo.currentText()
        group = self.ui.group_line.text()
        mark = self.ui.mark_line.text()
        self.callback(id_, name, was_present, group, mark)
        self.close()
