# contact form

import sys, os

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QComboBox, QTableView, QHeaderView, QVBoxLayout,
                             QHBoxLayout, QSizePolicy, QMessageBox) 
                             
from PyQt5.QtSql import (QSqlDatabase, QSqlRelationalTableModel, QSqlRelation,
                         QSqlRelation, QSqlRelationalDelegate, QSqlQuery)
from PyQt5.QtGui import QIcon

from PyQt5.QtCore import Qt

class PatientManager(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(1000, 500)
        self.setWindowTitle('Patient Management')

        self.createConnection()
        self.createTable()
        self.setupWidgets()

        self.show()

    def createConnection(self):
            
        database = QSqlDatabase.addDatabase("QSQLITE") # SQLite
        database.setDatabaseName("files/patients.db")

        if not database.open():
            print("Unable to open data patients.")
            sys.exit(1)

        tables_needed = {'patients'}
        tables_not_found = tables_needed - set(database.tables())
        if tables_not_found:
            QMessageBox.critical(None, 'Error',
                                 f'The following tables are missing from the database:{tables_not_found}')
                                 
            sys.exit(1)
       
    def createTable(self):

        self.model = QSqlRelationalTableModel()
        self.model.setTable('patients')

        self.model.setRelation(self.model.fieldIndex('diagnosis_id'),
        QSqlRelation('diagnosis','id', 'diagnos'))

        self.model.setHeaderData(self.model.fieldIndex('id'),
                                 Qt.Horizontal, 'ID')
        self.model.setHeaderData(self.model.fieldIndex('patient_id'),
                                 Qt.Horizontal, 'PATIENT')
        self.model.setHeaderData(self.model.fieldIndex('date'),
                                 Qt.Horizontal, 'DATE')
        self.model.setHeaderData(self.model.fieldIndex('sex'),
                                 Qt.Horizontal, 'SEX')
        self.model.setHeaderData(self.model.fieldIndex('incoming'),
                                 Qt.Horizontal, 'INCOMING')
        self.model.setHeaderData(self.model.fieldIndex('form'),
                                 Qt.Horizontal, 'FORM')
        self.model.setHeaderData(self.model.fieldIndex('diagnosis_id'),
                                 Qt.Horizontal, 'DIAGNOSIS')

        self.model.select()

    def setupWidgets(self):

        icons_path = "icons"

        title = QLabel("Patients Management System")
        title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")

        add_record_button = QPushButton("Add Patient")
#        add_record_button.setIcon(QIcon(os.path.join(icons_path, "add_user.png")))
        add_record_button.setStyleSheet("padding: 10px")
        add_record_button.clicked.connect(self.addRecord)

        del_record_button = QPushButton("Delete")
#        del_record_button.setIcon(QIcon(os.path.join(icons_path, "trash_can.png")))
        del_record_button.setStyleSheet("padding: 10px")
        del_record_button.clicked.connect(self.deleteRecord)

        sorting_options = ["Sort by ID", "Sort by HISTORY_PATIENT", "Sort by DATE",
                           "Sort by FIRST_NAME", "Sort by SEX", "Sort by INCOMING",
                           "Sort by FORM", "Sort by DIAGNOSIS"]

        sort_name_cb = QComboBox()
        sort_name_cb.addItems(sorting_options)
        sort_name_cb.currentTextChanged.connect(self.setSortingOrder)

        buttons_h_box = QHBoxLayout()
        buttons_h_box.addWidget(add_record_button)
        buttons_h_box.addWidget(del_record_button)
        buttons_h_box.addStretch()
        buttons_h_box.addWidget(sort_name_cb)

        edit_buttons = QWidget()
        edit_buttons.setLayout(buttons_h_box)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)

        delegate = QSqlRelationalDelegate(self.table_view)
        self.table_view.setItemDelegate(delegate)
        
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(title, Qt.AlignLeft)
        main_v_box.addWidget(edit_buttons)
        main_v_box.addWidget(self.table_view)
        self.setLayout(main_v_box)

    def addRecord(self):

        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = QSqlQuery()
        query.exec_("SELECT MAX (id) FROM patients")
        if query.next():
            id = int(query.value(0))

    def deleteRecord(self):

        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.select()

    def setSortingOrder(self, text):

        if text == "Sort by ID":
            self.model.setSort(self.model.fieldIndex('id'),
                               Qt.AscendingOrder)
        
        elif text == "Sort by HISTORY_PATIENT":
            self.model.setSort(self.model.fieldIndex('patient_id'),
                               Qt.AscendingOrder)

        elif text == "Sort by DATE":
            self.model.setSort(self.model.fieldIndex('date'),
                               Qt.AscendingOrder)

        elif text == "Sort by FIRST_NAME":
            self.model.setSort(self.model.fieldIndex('first_name'),
                               Qt.AscendingOrder)

        
        elif text == "Sort by SEX":
            self.model.setSort(self.model.fieldIndex('sex'),
                               Qt.AscendingOrder)

        elif text == "Sort by INCOMING":
            self.model.setSort(self.model.fieldIndex('incoming'),
                               Qt.AscendingOrder)

        elif text == "Sort by FORM":
            self.model.setSort(self.model.fieldIndex('form'),
                               Qt.AscendingOrder)

        elif text == "Sort by DIAGNOSIS":
            self.model.setSort(self.model.fieldIndex('diagnosis_id'),
                               Qt.AscendingOrder)
        
        self.model.select()
        
if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = PatientManager()
    sys.exit(app.exec_())













            

            
