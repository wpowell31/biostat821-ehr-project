"""
This module analyzes EHR records.

It analyzes both patient and lab information.
"""
from datetime import datetime

PATIENT_TYPE = dict[str, dict[str, str]]


def parse_patient_file(patient_filename: str) -> PATIENT_TYPE:
    """Parse through just the patient file."""
    patient_records = dict() #O(1)
    patient_file = open(patient_filename) #O(1)
    headers = patient_file.readline().strip().split("\t")#O(n) #chars in line1
    data = patient_file.readlines() #O(n) - n is num of chars in file
    patient_file.close() #O(1)

    # Parse rows and get records for each patient
    for patient in data: #O(n) n is number of patients
        patient_data = patient.split("\t") #O(n) n is #chars in the line
        patid = patient_data[0] #O(1)
        patient_records[patid] = dict(zip(headers[1:], patient_data[1:])) #O(1)
                                                            
    return patient_records #O(1)


LAB_TYPE = dict[str, list[dict[str, str]]]


def parse_lab_file(lab_filename: str) -> LAB_TYPE:
    """Parse through the patient file."""
    lab_records: dict[str, list[dict[str, str]]] = dict() #O(1)
    lab_file = open(lab_filename) #O(1)
    headers = lab_file.readline().strip().split("\t") #O(n) n chars in line1
    data = lab_file.readlines() #O(n) - n is # of chars in the file
    lab_file.close() #O(1)

    # Parse lab file and get individual lab records
    for lab in data: #O(n) n is number of labs
        lab_data = lab.split("\t") #O(n) n is number of characters in line
        patid = lab_data[0] #O(1)
        lab_records.setdefault(patid, []).append(
            dict(zip(headers[1:], lab_data[1:]))  #O(1)
        )

    return lab_records #O(1)


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    """Take in files and return dictionaries of data."""
    patient_records = parse_patient_file(patient_filename) #O(mn) m labs, 
                                                        #n characters in line
    lab_records = parse_lab_file(lab_filename) #O(mn) m patients, n chars

    return patient_records, lab_records #O(1)


def patient_age(records: dict[str, dict[str, str]], patient_id: str) -> int:
    """Calculate the age in years."""
    patient_birthday_str = records[patient_id]["PatientDateOfBirth"] #O(1)
    format = "%Y-%m-%d %H:%M:%S.%f" #O(1)
    patient_birthday = datetime.strptime(patient_birthday_str, format) #O(n)
                                                        #n is length of string
    current_time = datetime.now() #O(1)
    delta = current_time - patient_birthday #O(1)
    age = int(delta.days / 365.2425) #O(1)
    return age #O(1)


def patient_is_sick(
    records: dict[str, list[dict[str, str]]],
    patient_id: str,
    lab_name: str,
    operator: str,
    value: float,
) -> bool:
    """
    Take in patient records and determine relationship to threshold.

    Return boolean.
    """
    lab_records = records[patient_id]

    # Parsing that patient's labs of that type
    for lab in lab_records: #O(n) n is # of labs
        if lab["LabName"] == lab_name: #O(1)
            lab_value = lab["LabValue"] #O(1)
            # seeing if the lab value matches the sickness criterion
            if operator == "<": #O(1)
                if float(lab_value) < value: #O(1)
                    return True #O(1)
            if operator == ">": #O(1)
                if float(lab_value) > value: #O(1)
                    return True #O(1)
    return False #O(1)


def main() -> None:
    """Run the ehr-module."""
    patient_filename = "PatientCorePopulatedTable.txt"
    lab_filename = "LabsCorePopulatedTable.txt"

    patient_records, lab_records = parse_data(patient_filename, lab_filename)


if __name__ == "__main__":
    main()
