#!/usr/bin/python3
# -*- coding: utf-8 -*-
# create database

import sys, random


from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class CreatePatientData:

    database = QSqlDatabase.addDatabase("QSQLITE") # SQLite
    database.setDatabaseName("files/patients.db")

    if not database.open():
        print("Unable to open data patients.")
        sys.exit(1)

    query = QSqlQuery()
    query.exec_("DROP TABLE patients")
    query.exec_("DROP TABLE diagnosis")

    # Create patient table

    query.exec_("""CREATE TABLE patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                patient_id INTEGER NOT NULL,
                date INTEGER NOT NULL,
                first_name VARCHAR(30) NOT NULL,
                sex VARCHAR (6) NOT NULL,
                incoming VARCHAR (15) NOT NULL,
                form VARCHAR (10) NOT NULL,
                diagnosis_id VARCHAR (50) REFERENCES diagnosis(id))""")

    query.prepare("""INSERT INTO patients (
                    patient_id, date, first_name, sex,
                incoming, form, diagnosis_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)""")


    first_name = ["Петров", "Иванов", "Сидоров", "Пупкин",
                  "Тимофеев", "Путин", "Макрон", "Байден"]

    patient_id = [1, 2, 3, 4, 5, 6, 7, 8]

    sex = ["Male", "Female"]

    date = [12, 23, 25, 156, 846, 23]

    incoming = ["RECEPTION", "Surgery", "Trauma", "Therapy", "Gastro",
                            "Pulmo", "Cardio", "Neuro"]

    form = ["INCOMING", "Daily", "Consultation", "Epicrisis",
                            "Post-mortem"]

    diagnosis = {"ИБС": 1, "ЖКК": 2, "Политравма": 3, "Холецистит": 4, "Цирроз":5}

    diagnos_names = list(diagnosis.keys())
    diagnos_codes = list(diagnosis.values())

    for f_name in first_name:

        p_id = patient_id.pop()
        for_m = random.choice(form)
        d_t = random.choice(date)
        inc_m = random.choice(incoming)
        s_x = random.choice(sex)
        diagnosis_id = random.choice(diagnos_codes)

        query.addBindValue(p_id)
        query.addBindValue(d_t)
        query.addBindValue(f_name)
        query.addBindValue(s_x)
        query.addBindValue(inc_m)
        query.addBindValue(for_m)
        query.addBindValue(diagnosis_id)
        query.exec_()

        # Create diagnos table

    diagnos_query = QSqlQuery()
    diagnos_query.exec_("""CREATE TABLE diagnosis (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                diagnos VARCHAR(50) NOT NULL)""")
        
    diagnos_query.prepare("INSERT INTO diagnosis (diagnos) VALUES (?)")

    for name in diagnos_names:
        diagnos_query.addBindValue(name)
        diagnos_query.exec_()

    print("[INFO] Database successfully created.")

    sys.exit(0)
        

if __name__ == "__main__":
    CreatePatientData()
