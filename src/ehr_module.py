"""
This module analyzes EHR records.

It analyzes both patient and lab information.
"""
from datetime import datetime
import sqlite3
from fake_files import fake_files


class Lab:
    """Create the lab class."""

    def __init__(self, PatientID: str, LabID: str) -> None:
        """Initialize the lab class."""
        self.PatientID = PatientID
        self.LabID = LabID

    @property
    def LabName(self) -> str:
        """Define LabName property."""
        connection = sqlite3.connect("ehr_database.db")
        cursor = connection.cursor()
        lab_name = cursor.execute(
            f"""SELECT LabName
            FROM labs
            WHERE LabID='{self.LabID}'"""
        ).fetchall()
        return str(lab_name[0][0])

    @property
    def LabValue(self) -> str:
        """Define LabValue property."""
        connection = sqlite3.connect("ehr_database.db")
        cursor = connection.cursor()
        print(self.PatientID)
        lab_value = cursor.execute(
            f"""SELECT LabValue
            FROM labs
            WHERE LabID='{self.LabID}'"""
        ).fetchall()
        return str(lab_value[0][0])

    @property
    def LabUnits(self) -> str:
        """Define LabUnits property."""
        connection = sqlite3.connect("ehr_database.db")
        cursor = connection.cursor()
        lab_units = cursor.execute(
            f"""SELECT LabUnits
            FROM labs
            WHERE LabID='{self.LabID}'"""
        ).fetchall()
        return str(lab_units[0][0])

    @property
    def LabDateTime(self) -> datetime:
        """Calculate the date of the lab."""
        connection = sqlite3.connect("ehr_database.db")
        cursor = connection.cursor()
        lab_date_raw = cursor.execute(
            f"""
            SELECT LabDateTime
            FROM labs
            WHERE LabID='{self.LabID}'"""
        ).fetchall()
        lab_date_str = str(lab_date_raw[0][0])
        format = "%Y-%m-%d %H:%M:%S.%f"
        lab_date = datetime.strptime(lab_date_str, format)

        return lab_date


class Patient:
    """Create the patient class."""

    def __init__(self, patient_id: str, patient_labs: list[Lab]) -> None:
        """Intiialize the patient."""
        self.patient_id = patient_id
        self.patient_labs = patient_labs

    @property
    def age(self) -> int:
        """Calculate the age in years."""
        connection = sqlite3.connect("ehr_database.db")
        cursor = connection.cursor()

        patient_birthday_raw = cursor.execute(
            f"""SELECT PatientDateOfBirth
            FROM patients
            WHERE PatientID='{self.patient_id}'"""
        ).fetchall()
        patient_birthday_str: str = str(patient_birthday_raw[0][0])

        format = "%Y-%m-%d %H:%M:%S.%f"
        patient_birthday = datetime.strptime(patient_birthday_str, format)
        current_time = datetime.now()
        delta = current_time - patient_birthday
        age = int(delta.days / 365.2425)
        connection.close()
        return age

    def is_sick(
        self,
        lab_name: str,
        operator: str,
        value: float,
    ) -> bool:
        """
        Take in patient records and determine relationship to threshold.

        Return boolean.
        """
        connection = sqlite3.connect("ehr_database.db")
        cursor = connection.cursor()

        lab_values = self.patient_labs
        float_values = [
            float(lab_values[i].LabValue) for i in range(len(lab_values))
        ]
        if operator == "<":
            if min(float_values) < value:
                return True
        if operator == ">":
            if max(float_values) > value:
                return True
        return False

    def initial_age(self) -> int:
        """Calculate patient age for initial lab record."""
        connection = sqlite3.connect("ehr_database.db")
        cursor = connection.cursor()
        # Finding the birthday for the patient
        format = "%Y-%m-%d %H:%M:%S.%f"  # O(1)
        patient_birthday_raw = cursor.execute(
            f"""SELECT PatientDateOfBirth
            FROM Patients
            WHERE PatientID='{self.patient_id}'"""
        ).fetchall()
        patient_birthday_str = str(patient_birthday_raw[0][0])
        patient_birthday = datetime.strptime(patient_birthday_str, format)

        min_date_raw = cursor.execute(
            f"""SELECT MIN(LabDateTime)
            FROM labs
            WHERE PatientID='{self.patient_id}'"""
        ).fetchall()
        min_date2 = min_date_raw[0][0]
        min_date = datetime.strptime(min_date2, format)
        delta = min_date - patient_birthday
        age = int(delta.days / 365.2425)

        return age


def parse_lab_file(lab_filename: str) -> list[Lab]:
    """Parse through the lab file."""
    connection = sqlite3.connect("ehr_database.db")
    cursor = connection.cursor()

    # Read File
    lab_file = open(lab_filename)  # O(1)
    headers = lab_file.readline().strip().split("\t")  # O(q)
    data = lab_file.readlines()  # O(pq)
    lab_file.close()

    # Parse lab file and get individual lab records
    labs: list[Lab] = []
    lab_id = 0
    for lab in data:
        # Creating a Lab Class instance with Patient idea
        lab_data = lab.split("\t")
        lab_dict = dict(zip(headers, lab_data))
        # Storing the rest of the lab data in the SQL database
        cursor.executemany(
            """INSERT INTO labs (PatientID,
                                AdmissionID,
                                LabName,
                                LabValue,
                                LabUnits,
                                LabDateTime,
                                LabID)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    lab_dict["PatientID"],
                    lab_dict["AdmissionID"],
                    lab_dict["LabName"],
                    lab_dict["LabValue"],
                    lab_dict["LabUnits"],
                    lab_dict["LabDateTime"],
                    str(lab_id),
                )
            ],
        )

        labs.append(Lab(lab_dict["PatientID"], str(lab_id)))
        lab_id += 1
    connection.commit()
    connection.close()

    return labs


def parse_patient_file(
    patient_filename: str, lab_records: list[Lab]
) -> list[Patient]:
    """Parse through just the patient file."""
    connection = sqlite3.connect("ehr_database.db")
    cursor = connection.cursor()

    # Read file
    patient_file = open(patient_filename)  # O(1)
    headers = (
        patient_file.readline().strip().split("\t")
    )  # O(n) #chars in line1
    data = patient_file.readlines()  # O(mn) - reads entire file
    patient_file.close()  # O(1)

    # Parse through labs and make dictionary
    labs_dict: dict[str, list[Lab]] = dict()
    for lab in lab_records:
        labs_dict.setdefault(lab.PatientID, []).append(lab)

    # Parse rows and get records for each patient
    patient_records = []
    for patient in data:
        patient_data = patient.split("\t")
        patient_records_dict = dict(zip(headers, patient_data))
        print(labs_dict)
        patient_labs: list[Lab] = labs_dict[patient_records_dict["PatientID"]]
        patientClass = Patient(patient_records_dict["PatientID"], patient_labs)

        patient_records.append(patientClass)
        cursor.executemany(
            "INSERT INTO patients Values(?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    patient_records_dict["PatientID"],
                    patient_records_dict["PatientGender"],
                    patient_records_dict["PatientDateOfBirth"],
                    patient_records_dict["PatientRace"],
                    patient_records_dict["PatientMaritalStatus"],
                    patient_records_dict["PatientLanguage"],
                    patient_records_dict[
                        "PatientPopulationPercentageBelowPoverty"
                    ],
                )
            ],
        )
    connection.commit()
    connection.close()

    return patient_records


def parse_data(patient_filename: str, lab_filename: str) -> list[Patient]:
    """Take in files and return dictionaries of data."""
    connection = sqlite3.connect("ehr_database.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS patients")
    cursor.execute("DROP TABLE IF EXISTS labs")

    cursor.execute(
        """CREATE TABLE patients
                (PatientID VARCHAR,
                PatientGender VARCHAR,
                PatientDateOfBirth VARCHAR,
                PatientRace VARCHAR,
                PatientMaritalStatus VARCHAR,
                PatientLanguage VARCHAR,
                PatientPopulationPercentageBelowPoverty VARCHAR)"""
    )

    cursor.execute(
        """CREATE TABLE labs
                (PatientID VARCHAR,
                AdmissionID VARCHAR,
                LabName VARCHAR,
                LabValue VARCHAR,
                LabUnits VARCHAR,
                LabDateTime VARCHAR,
                LabID VARCHAR)"""
    )
    lab_records = parse_lab_file(lab_filename)
    patient_records = parse_patient_file(patient_filename, lab_records)

    return patient_records


def main() -> None:
    """Run the ehr-module."""


if __name__ == "__main__":
    main()
