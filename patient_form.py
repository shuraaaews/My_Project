# contact form

import sys

from PyQt5.QtWidgets import (QAction, QApplication, QWidget, QLabel, QPushButton,
                             QDialog, QTabWidget, QMessageBox, QLineEdit, QHBoxLayout,
                             QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton,
                             QGridLayout)
from PyQt5.QtGui import (QIntValidator, QFont, QIcon, QKeySequence, QTextCharFormat,
        QTextCursor, QTextTableFormat)

from PyQt5.QtCore import Qt, QSize


class ContactForm(QWidget):

        def __init__(self):
            super().__init__()
            self.initializeUI()

        def initializeUI(self):
            self.setGeometry(100, 100, 400, 300)
            self.setWindowTitle('Patient Form')

            self.setupTabs()

            self.show()

        def setupTabs(self):

            self.tab_bar = QTabWidget(self)

            self.prof_details_tab = QWidget()
            self.background_tab = QWidget()

            self.tab_bar.addTab(self.prof_details_tab, "Profile Details")
            self.tab_bar.addTab(self.background_tab, "Background")

            self.profileDetailsTab()
            self.backgroundTab()

            main_h_box = QHBoxLayout()
            main_h_box.addWidget(self.tab_bar)

            self.setLayout(main_h_box)

        def profileDetailsTab(self):

           
            history_label = QLabel("№ History")
            history_entry = QLineEdit()
            history_entry.setInputMask("№ 000000\/00;_")
            history_entry.setMaximumWidth(100)

            name_label = QLabel("Name")
            name_entry = QLineEdit()

            age_label = QLabel("Age")
            age_entry = QLineEdit()
            age_entry.setMaximumWidth(40)
            age_entry.setValidator(QIntValidator(0, 100))
            
            sex_gb = QGroupBox("Sex")

            male_rb = QRadioButton("Male")
            female_rb = QRadioButton("Female")

            sex_h_box = QHBoxLayout()
            sex_h_box.addWidget(male_rb)
            sex_h_box.addWidget(female_rb)
            
            sex_gb.setLayout(sex_h_box)
            
            n_h = QWidget()
            name_h_box = QHBoxLayout()
                        
            name_h_box.addWidget(history_label)
            name_h_box.addWidget(history_entry)

            name_h_box.addWidget(name_label)
            name_h_box.addWidget(name_entry)

            name_h_box.addWidget(age_label)
            name_h_box.addWidget(age_entry)

            name_h_box.addWidget(sex_gb)
            n_h.setLayout(name_h_box)

            tab_v_box = QVBoxLayout()
            tab_v_box.addWidget(n_h)
            
            self.arrival_gb = QGroupBox("Arrival from")

            arr_h_box = QHBoxLayout()

            arrival_list = ["RECEPTION", "Surgery", "Trauma", "Therapy", "Gastro",
                            "Pulmo", "Cardio", "Neuro", "Urologi", "Ginecologi"]

            for ar in arrival_list:
                self.arrival_rb = QRadioButton(ar)
                arr_h_box.addWidget(self.arrival_rb)

            self.arrival_gb.setLayout(arr_h_box)


            tab_v_box.addWidget(self.arrival_gb)


            tab_v_box.addStretch()



            self.form_gb = QGroupBox("Form")

            form_h_box = QHBoxLayout()

            form_list = ["INCOMING", "Daily", "Consultation", "Epicrisis",
                            "Post-mortem"]
            for fr in form_list:
                self.form_rb = QRadioButton(fr)
                form_h_box.addWidget(self.form_rb)

            self.form_gb.setLayout(form_h_box)

            tab_v_box.addWidget(self.form_gb)
            tab_v_box.addStretch()


            start_form_button = QPushButton("Start")
            tab_v_box.addWidget(start_form_button, alignment=Qt.AlignRight)

            self.prof_details_tab.setLayout(tab_v_box)

        def backgroundTab(self):

            pass

          

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    window = ContactForm()
    sys.exit(app.exec_())













            

            
