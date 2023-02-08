"""
This module analyzes EHR records.

It analyzes both patient and lab information.
"""
from datetime import datetime

PATIENT_TYPE = dict[str, dict[str, str]]


def parse_patient_file(patient_filename: str) -> PATIENT_TYPE:
    """Parse through just the patient file."""
    patient_records = dict()
    patient_file = open(patient_filename)
    headers = patient_file.readline().strip().split("\t")
    data = patient_file.readlines()
    patient_file.close()

    # Parse rows and get records for each patient
    for patient in data:
        patient_data = patient.split("\t")
        patid = patient_data[0]
        patient_records[patid] = dict(zip(headers[1:], patient_data[1:]))

    return patient_records


LAB_TYPE = dict[str, list[dict[str, str]]]


def parse_lab_file(lab_filename: str) -> LAB_TYPE:
    """Parse through the patient file."""
    lab_records: dict[str, list[dict[str, str]]] = dict()
    lab_file = open(lab_filename)
    headers = lab_file.readline().strip().split("\t")
    data = lab_file.readlines()
    lab_file.close()

    # Parse lab file and get individual lab records
    for lab in data:
        lab_data = lab.split("\t")
        patid = lab_data[0]
        lab_records.setdefault(patid, []).append(
            dict(zip(headers[1:], lab_data[1:]))
        )

    return lab_records


def parse_data(
    patient_filename: str, lab_filename: str
) -> tuple[dict[str, dict[str, str]], dict[str, list[dict[str, str]]]]:
    """Take in files and return dictionaries of data."""
    patient_records = parse_patient_file(patient_filename)
    lab_records = parse_lab_file(lab_filename)

    return patient_records, lab_records


def patient_age(records: dict[str, dict[str, str]], patient_id: str) -> int:
    """Calculate the age in years."""
    patient_birthday_str = records[patient_id]["PatientDateOfBirth"]
    format = "%Y-%m-%d %H:%M:%S.%f"
    patient_birthday = datetime.strptime(patient_birthday_str, format)
    current_time = datetime.now()
    delta = current_time - patient_birthday
    age = int(delta.days / 365.2425)
    return age


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
    for lab in lab_records:
        if lab["LabName"] == lab_name:
            lab_value = lab["LabValue"]
            # seeing if the lab value matches the sickness criterion
            if operator == "<":
                if float(lab_value) < value:
                    return True
            if operator == ">":
                if float(lab_value) > value:
                    return True
    return False


def main() -> None:
    """Run the ehr-module."""
    patient_filename = "PatientCorePopulatedTable.txt"
    lab_filename = "LabsCorePopulatedTable.txt"

    patient_records, lab_records = parse_data(patient_filename, lab_filename)


if __name__ == "__main__":
    main()
