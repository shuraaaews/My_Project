# contact form

import sys, random, time

from PyQt5.QtWidgets import (QAction, QApplication, QWidget, QLabel, QPushButton, QButtonGroup,
                             QDialog, QTabWidget, QMessageBox, QLineEdit, QHBoxLayout,
                             QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton,
                             QGridLayout, QSizePolicy, QComboBox, QTableView, QHeaderView,
                             QMessageBox, QCheckBox)
from PyQt5.QtGui import (QIntValidator, QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)

from PyQt5.QtSql import (QSqlDatabase, QSqlRelationalTableModel, QSqlRelation,
                         QSqlRelation, QSqlRelationalDelegate, QSqlQuery,
                         QSqlDatabase, QSqlTableModel)

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

from PyQt5.QtCore import Qt, QSize

key_list = set ()





class PatientManager(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
   #     self.setMinimumSize(1000, 500)
   #     self.setWindowTitle('Patient Management')

        self.createConnection()
        self.createTable()
        self.setupWidgets()


        self.show()

    def createConnection(self):


        database = QSqlDatabase.addDatabase("QSQLITE") # SQLite
        database.setDatabaseName("files/patients.db")

        print(database.open())
        if not database.open():
            print("Unable to open data patients.")
            sys.exit(1)

        print('4',database.contains("files/patients.db"))
        query = QSqlQuery(database)
        #query.exec_("DROP TABLE patients")
       # query.exec_("DROP TABLE diagnosis")

        # Create patient table

        query.exec_("""CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    patient_id VARCHAR NOT NULL,
                    date VARCHAR NOT NULL,
                    first_name VARCHAR(30) NOT NULL,
                    sex VARCHAR (6) NOT NULL,
                    age VARCHAR (3) NOT NULL,
                    profile VARCHAR (15) NOT NULL,
                    form VARCHAR (10) NOT NULL,
                    diagnosis_id VARCHAR (50) NOT NULL)""")



        query.prepare("""INSERT INTO patients (
                        patient_id, date, first_name, sex, age,
                    profile, form, diagnosis_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""")


        
        query.exec_()
        print("[INFO] Database successfully created.")

        

        tables_needed = {'patients'}
        tables_not_found = tables_needed - set(database.tables())
        if tables_not_found:
            QMessageBox.critical(None, 'Error',
                                 f'The following tables are missing from the database:{tables_not_found}')
                                 
            sys.exit(1)

        
       
    def addRecord(self, SS):


        database = QSqlDatabase.addDatabase("QSQLITE") # SQLite
        database.setDatabaseName("files/patients.db")
        print('2',database.isOpen())
        database.open()
        if not database.open():
            print("Unable to open data patients.")
            sys.exit(1)



        print('3',database.isOpen())
        print('4',database.contains("files/patients.db"))
        print('5',database.connectionNames())
        print('this:  ',SS)

        for i in range(8):
            print(SS[i], type(SS[i]), i)
            
        query = QSqlQuery()
                                                                                                                                        
        query.prepare("""INSERT INTO patients (
                        patient_id, date, first_name, sex, age,
                    profile, form, diagnosis_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""")

        
        
        query.exec_()

        
        query.addBindValue(SS[0])
        print(SS[2])
            
        query.addBindValue(SS[1])
        query.addBindValue(SS[2])
        query.addBindValue(SS[3])
        query.addBindValue(SS[4])
        query.addBindValue(SS[5])
        query.addBindValue(SS[6])
        query.addBindValue(SS[7])
        query.exec_()



    def deleteRecord(self):

        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.select()



    def createTable(self):

        self.model = QSqlTableModel()
        self.model.setTable('patients')
        self.model.setEditStrategy(0)
        #self.model.resizeColumnToContents()
        #self.model.setRelation(self.model.fieldIndex('diagnosis_id'),
        #QSqlRelation('diagnosis','id', 'diagnos'))

        self.model.setHeaderData(self.model.fieldIndex('id'),
                                 Qt.Horizontal, 'ID')
        self.model.setHeaderData(self.model.fieldIndex('patient_id'),
                                 Qt.Horizontal, 'HISTORY_PATIENT')
        self.model.setHeaderData(self.model.fieldIndex('date'),
                                 Qt.Horizontal, 'DATE')
        self.model.setHeaderData(self.model.fieldIndex('first_name'),
                                 Qt.Horizontal, 'FIRST_NAME')
        self.model.setHeaderData(self.model.fieldIndex('sex'),
                                 Qt.Horizontal, 'SEX')
        self.model.setHeaderData(self.model.fieldIndex('age'),
                                 Qt.Horizontal, 'AGE')
        self.model.setHeaderData(self.model.fieldIndex('profile'),
                                 Qt.Horizontal, 'PROFILE')
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
                           "Sort by FIRST_NAME", "Sort by SEX", "Sort by AGE", "Sort by PROFILE",
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
        self.table_view.setColumnHidden(0, True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(1,3)
        self.table_view.horizontalHeader().setSectionResizeMode(0,3)
        self.table_view.horizontalHeader().setSectionResizeMode(2,3)
        self.table_view.horizontalHeader().setSectionResizeMode(4,3)
        self.table_view.horizontalHeader().setSectionResizeMode(5,3)
        self.table_view.horizontalHeader().setSectionResizeMode(6,3)
        self.table_view.horizontalHeader().setSectionResizeMode(7,3)
        self.table_view.setGridStyle(5)
        self.table_view.setAlternatingRowColors(True)
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

        elif text == "Sort by AGE":
            self.model.setSort(self.model.fieldIndex('age'),
                               Qt.AscendingOrder)


        elif text == "Sort by PROFILE":
            self.model.setSort(self.model.fieldIndex('profile'),
                               Qt.AscendingOrder)

        elif text == "Sort by FORM":
            self.model.setSort(self.model.fieldIndex('form'),
                               Qt.AscendingOrder)

        elif text == "Sort by DIAGNOSIS":
            self.model.setSort(self.model.fieldIndex('diagnosis_id'),
                               Qt.AscendingOrder)
        
        self.model.select()
          



class ContactForm(QWidget):

    def __init__(self):
        super().__init__()
    #    self.w = None
        self.initializeUI()

    def initializeUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setMinimumSize(1100, 500)
        self.setWindowTitle('Patient Form')
        self.w = PatientManager()
        self.setupTabs()

        self.show()

    def setupTabs(self):

        self.tab_bar = QTabWidget(self)

        self.prof_details_tab = QWidget()
        self.background_tab = QWidget()

        self.tab_bar.addTab(self.prof_details_tab, "Profile Details")
        self.tab_bar.addTab(self.w, "Background")
#        self.tab_bar.addTab(self.background_tab, "Background")

        self.profileDetailsTab()
        self.tab_bar.setTabPosition(0)
        self.tab_bar.setTabShape(0)
        self.tab_bar.setDocumentMode(False)
        self.tab_bar.setTabToolTip(1, """patients
                                            who are exist
                                        _________________""")
        self.tab_bar.setTabEnabled(0, True)
        self.tab_bar.setCurrentWidget(QTableView())
        self.tab_bar.setCurrentIndex(0)

        self.backgroundTab()

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.tab_bar)

        self.setLayout(main_h_box)

    def profileDetailsTab(self):


        now = time.localtime()
        print(now)
        print(time.strftime("%d %m %Y", now))
        date_now = time.strftime("%d.%m.%Y", now)
        time_now = time.strftime("%H-%M", now)

        date_label = QLabel("Date")
        self.date_entry = QLineEdit()
        self.date_entry.setMaximumWidth(82)
        time_label = QLabel("Time")
        self.time_entry = QLineEdit()
        self.time_entry.setMaximumWidth(45)

        self.date_entry.setInputMask("99.B9.9999")
        #self.date_entry.setPlaceholderText(date_now)
        self.date_entry.setText(date_now)
        self.time_entry.setInputMask("99-99")
        self.time_entry.setText(time_now)
        #self.time_entry.setPlaceholderText(time_now)
        d_h = QWidget()
        date_h_box = QHBoxLayout()
        date_h_box.addWidget(date_label)
        date_h_box.addWidget(self.date_entry)
        date_h_box.addWidget(time_label)
        date_h_box.addWidget(self.time_entry)

        d_h.setLayout(date_h_box)
        date_h_box.addStretch()
        
           
        history_label = QLabel("№ History")
        self.history_entry = QLineEdit()
        self.history_entry.setInputMask("№ 000000\/00;_")
        self.history_entry.setMaximumWidth(100)
        self.history_entry.textEdited.connect(self.history_entry_text)
    
        name_label = QLabel("Name")
        self.name_entry = QLineEdit()
        self.name_entry.textChanged.connect(self.name_entry_text)

        age_label = QLabel("Age")
        self.age_entry = QLineEdit()
        self.age_entry.setMaximumWidth(40)
        self.age_entry.setValidator(QIntValidator(0, 100))
        self.age_entry.textChanged.connect(self.age_entry_text)
            
        sex_gb = QGroupBox("Sex")

        self.male_rb = QRadioButton("Male")
        self.female_rb = QRadioButton("Female")
        self.male_rb.click()

        sex_h_box = QHBoxLayout()
        sex_h_box.addWidget(self.male_rb)
        sex_h_box.addWidget(self.female_rb)
            
        sex_gb.setLayout(sex_h_box)
            
        n_h = QWidget()
        name_h_box = QHBoxLayout()
                        
        name_h_box.addWidget(history_label)
        name_h_box.addWidget(self.history_entry)

        name_h_box.addWidget(name_label)
        name_h_box.addWidget(self.name_entry)

        name_h_box.addWidget(age_label)
        name_h_box.addWidget(self.age_entry)

        name_h_box.addWidget(sex_gb)
        n_h.setLayout(name_h_box)

        tab_v_box = QVBoxLayout()
        tab_v_box.addWidget(d_h)
        tab_v_box.addWidget(n_h)
            

        profile_gbox = QGroupBox("Profile")
        self.profile_group_botton = QButtonGroup()

        profile_h_box = QHBoxLayout()

        profile_list = ["Surgery", "Therapy"]

        for ar in profile_list:
            profile_rb = QRadioButton(ar)
            profile_h_box.addWidget(profile_rb)
            self.profile_group_botton.addButton(profile_rb)

        profile_rb.setChecked(True)
        profile_gbox.setLayout(profile_h_box)


        tab_v_box.addWidget(profile_gbox)
        profile_h_box.addStretch()
        tab_v_box.addStretch()

        
        key_gbox = QGroupBox("Key words")

        key_grid_box = QGridLayout()

        key_list = ["RECEPTION", "Surgery", "Trauma", "Neurosurgery","Ginecology",
                        "Therapy","Cardio", "Neuro", "Pulmo", "Gastro", "Pediatric",
                           "Mortem", "IVL", "Critical"]

        positions = [(i, j) for i in range(3) for j in range(5)]


        for position, name in zip(positions, key_list):

            self.key_rb = QCheckBox(name)
            key_grid_box.addWidget(self.key_rb, *position)

            self.key_rb.setChecked(False)

            self.key_rb.stateChanged.connect(self.printCh)

        key_gbox.setLayout(key_grid_box)
        

        tab_v_box.addWidget(key_gbox)


        tab_v_box.addStretch()



        


        form_gbox = QGroupBox("Form")
        self.form_group_botton = QButtonGroup()
        form_h_box = QHBoxLayout()

        form_list = ["INCOMING", "Daily", "Consultation", "Epicrisis",
                            "Post-mortem"]
        for fr in form_list:
            form_rb = QRadioButton(fr)
            form_h_box.addWidget(form_rb)
            self.form_group_botton.addButton(form_rb)
            
        
        form_rb.setChecked(True)
        form_gbox.setLayout(form_h_box)

        tab_v_box.addWidget(form_gbox)
        tab_v_box.addStretch()
        

        start_form_button = QPushButton("Start")
        tab_v_box.addWidget(start_form_button, alignment=Qt.AlignRight)
        start_form_button.clicked.connect(self.start_form_button_clicked)

        self.prof_details_tab.setLayout(tab_v_box)
        form_h_box.addStretch()

    def name_entry_text(self, s):
        print(s)
        
    def age_entry_text(self, s):
        print(s)
      
    def history_entry_text(self, s):
        print(s)

    def start_form_button_clicked(self):

        date_entry = self.date_entry.text()
        history_entry = self.history_entry.text()
        name_entry = self.name_entry.text()
        age_entry = self.age_entry.text()

        if history_entry=='№ /' or name_entry=='' or age_entry == '':
            QMessageBox.information(self, "Error",
                    "Empty field !!! Try again", QMessageBox.Ok)
            return

        form_entry = self.form_group_botton.checkedButton().text()
        profile_entry = self.profile_group_botton.checkedButton().text()

        if self.male_rb.isChecked():
            sex_entry = self.male_rb.text()
        else:
            sex_entry = self.female_rb.text()

        diagnos = "pneumon"

        dd = ([x.text() for x in key_list ])
        print(dd)

        SS = [history_entry,date_entry,name_entry,sex_entry,age_entry,profile_entry,form_entry,diagnos]
        PatientManager.addRecord(self,SS)



    def printCh(self, s):

        if s == 2:
            s = self.sender() 
            key_list.add(s)

        else:
            s = self.sender() 
            key_list.remove(s)

    def backgroundTab(self):

        pass


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = ContactForm()
    sys.exit(app.exec_())













            

            
