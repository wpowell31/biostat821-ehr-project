"""
This module analyzes EHR records.

It analyzes both patient and lab information.
"""
from datetime import datetime


class Lab:
    """Create the lab class."""

    def __init__(
        self,
        patient_id: str,
        admission_id: str,
        lab_name: str,
        lab_value: str,
        lab_units: str,
        lab_date_time: str,
    ) -> None:
        """Initialize the lab class."""
        self.patient_id = patient_id
        self.admission_id = admission_id
        self.lab_name = lab_name
        self.lab_value = lab_value
        self.lab_units = lab_units
        self.lab_date_time = lab_date_time


class Patient:
    """Create the patient class."""

    def __init__(
        self,
        patient_id: str,
        patient_gender: str,
        patient_dob: str,
        patient_race: str,
        patient_marital_status: str,
        patient_language: str,
        patient_poverty: str,
        patient_labs: list[Lab],
    ) -> None:
        """Intiialize the patient."""
        self.patient_id = patient_id
        self.patient_gender = patient_gender
        self.patient_dob = patient_dob
        self.patient_race = patient_race
        self.patient_marital_status = patient_marital_status
        self.patient_language = patient_language
        self.patient_poverty = patient_poverty
        self.patient_labs = patient_labs

    @property
    def age(self) -> int:
        """Calculate the age in years."""
        patient_birthday_str = self.patient_dob
        format = "%Y-%m-%d %H:%M:%S.%f"
        patient_birthday = datetime.strptime(patient_birthday_str, format)
        current_time = datetime.now()
        delta = current_time - patient_birthday
        age = int(delta.days / 365.2425)
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
        lab_records = self.patient_labs

        # Parsing that patient's labs of that type
        for lab in lab_records:  # O(p/m) p is # of labs, m patients
            if lab.lab_name == lab_name:  # O(1)
                lab_value = lab.lab_value  # O(1)
                # seeing if the lab value matches the sickness criterion
                if operator == "<":  # O(1)
                    if float(lab_value) < value:  # O(1)
                        return True  # O(1)
                if operator == ">":  # O(1)
                    if float(lab_value) > value:  # O(1)
                        return True  # O(1)
        return False  # O(1)

    def initial_age(self) -> int:
        """Calculate patient age for initial lab record."""
        # Getting Lab records for the patient
        patient_lab_records = self.patient_labs

        # Finding the birthday for the patient
        format = "%Y-%m-%d %H:%M:%S.%f"  # O(1)
        patient_birthday_str = self.patient_dob
        patient_birthday = datetime.strptime(patient_birthday_str, format)

        # Initializing
        min_date = datetime.now()
        age = 0

        # Parsing the lab records to find the lab record with the min date
        for lab in patient_lab_records:
            lab_date_str = lab.lab_date_time
            lab_date = datetime.strptime(lab_date_str, format)

            # Updating if this lab is the initial lab
            if lab_date < min_date:
                min_date = lab_date
                delta = min_date - patient_birthday
                age = int(delta.days / 365.2425)

        return age


def parse_lab_file(lab_filename: str) -> list[Lab]:
    """Parse through the patient file."""
    lab_file = open(lab_filename)  # O(1)
    headers = lab_file.readline().strip().split("\t")  # O(q)
    data = lab_file.readlines()  # O(pq)
    lab_file.close()  # O(1)

    # Parse lab file and get individual lab records
    lab_records = []
    for lab in data:
        lab_data = lab.split("\t")
        lab_dict = dict(zip(headers, lab_data))
        lab_class = Lab(
            lab_dict["PatientID"],
            lab_dict["AdmissionID"],
            lab_dict["LabName"],
            lab_dict["LabValue"],
            lab_dict["LabUnits"],
            lab_dict["LabDateTime"],
        )
        lab_records.append(lab_class)

    return lab_records


def parse_patient_file(
    patient_filename: str, lab_records: list[Lab]
) -> list[Patient]:
    """Parse through just the patient file."""
    patient_file = open(patient_filename)  # O(1)
    headers = (
        patient_file.readline().strip().split("\t")
    )  # O(n) #chars in line1
    data = patient_file.readlines()  # O(mn) - reads entire file
    patient_file.close()  # O(1)

    # Parse through labs and make dictionary
    labs_dict: dict[str, list[Lab]] = dict()
    for lab in lab_records:
        labs_dict.setdefault(lab.patient_id, []).append(lab)

    # Parse rows and get records for each patient
    patient_records = []
    for patient in data:
        patient_data = patient.split("\t")
        patient_records_dict = dict(zip(headers, patient_data))
        patient_labs: list[Lab] = labs_dict[patient_records_dict["PatientID"]]
        patientClass = Patient(
            patient_records_dict["PatientID"],
            patient_records_dict["PatientGender"],
            patient_records_dict["PatientDateOfBirth"],
            patient_records_dict["PatientRace"],
            patient_records_dict["PatientMaritalStatus"],
            patient_records_dict["PatientLanguage"],
            patient_records_dict["PatientPopulationPercentageBelowPoverty"],
            patient_labs,
        )

        patient_records.append(patientClass)

    return patient_records


def parse_data(patient_filename: str, lab_filename: str) -> list[Patient]:
    """Take in files and return dictionaries of data."""
    lab_records = parse_lab_file(lab_filename)
    patient_records = parse_patient_file(patient_filename, lab_records)

    return patient_records


def main() -> None:
    """Run the ehr-module."""
    patient_filename = "PatientCorePopulatedTable.txt"
    lab_filename = "LabsCorePopulatedTable.txt"

    patient_records, lab_records = parse_data(patient_filename, lab_filename)


if __name__ == "__main__":
    main()
