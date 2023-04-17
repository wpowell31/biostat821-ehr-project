"""Testing the EHR module."""
from ehr_module import parse_data
import ehr_module
from ehr_module import Patient, Lab
from fake_files import fake_files
import sqlite3


def test_parse_data_Patients() -> None:
    """Test the parse data function for correct Patient information."""

    fake_patient = [
        [
            "PatientID",
            "PatientGender",
            "PatientDateOfBirth",
            "PatientRace",
            "PatientMaritalStatus",
            "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty",
        ],
        [
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
            "Male",
            "1947-12-28 02:45:40.547",
            "Unknown",
            "Married",
            "Icelandic",
            "18.08",
        ],
    ]

    fake_lab = [
        [
            "PatientID",
            "AdmissionID",
            "LabName",
            "LabValue",
            "LabUnits",
            "LabDateTime",
        ],
        [
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
            "1",
            "URINALYSIS: RED BLOOD CELLS",
            "1.8",
            "rbc/hpf",
            "1992-07-01 01:36:17.910",
        ],
    ]
    with fake_files(fake_patient, fake_lab) as filenames:
        patient_records = parse_data(filenames[0], filenames[1])
        patient = patient_records[0]
        assert patient.patient_id == "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"


def test_parse_data_Labs() -> None:
    """Test the parse data function for correct Labs."""

    fake_patient = [
        [
            "PatientID",
            "PatientGender",
            "PatientDateOfBirth",
            "PatientRace",
            "PatientMaritalStatus",
            "PatientLanguage",
            "PatientPopulationPercentageBelowPoverty",
        ],
        [
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
            "Male",
            "1947-12-28 02:45:40.547",
            "Unknown",
            "Married",
            "Icelandic",
            "18.08",
        ],
    ]

    fake_lab = [
        [
            "PatientID",
            "AdmissionID",
            "LabName",
            "LabValue",
            "LabUnits",
            "LabDateTime",
        ],
        [
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
            "1",
            "URINALYSIS: RED BLOOD CELLS",
            "1.8",
            "rbc/hpf",
            "1992-07-01 01:36:17.910",
        ],
        [
            "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
            "1",
            "URINALYSIS: RED BLOOD CELLS",
            "3.2",
            "rbc/hpf",
            "1992-07-01 01:36:17.910",
        ],
    ]
    with fake_files(fake_patient, fake_lab) as filenames:
        patient_records = parse_data(filenames[0], filenames[1])
        patient = patient_records[0]
        lab_1 = patient.patient_labs[0]
        lab_2 = patient.patient_labs[1]
        assert lab_1.LabValue == "1.8"
        assert lab_2.LabValue == "3.2"


def test_patient_age() -> None:
    """Test patient age."""
    connection = sqlite3.connect("test_patient_age_database.db")
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

    cursor.executemany(
        "INSERT INTO patients Values(?, ?, ?, ?, ?, ?, ?)",
        [
            (
                "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
                "Male",
                "1947-12-28 02:45:40.547",
                "Unknown",
                "Married",
                "Icelandic",
                "18.08",
            )
        ],
    )

    cursor.executemany(
        "INSERT INTO labs Values(?, ?, ?, ?, ?, ?, ?)",
        [
            (
                "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
                "1",
                "URINALYSIS: RED BLOOD CELLS",
                "1.8",
                "rbc/hpf",
                "1992-07-01 01:36:17.910",
                "0",
            )
        ],
    )
    connection.commit()
    lab_1 = Lab("FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "0")
    patient = Patient("FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", [lab_1])

    assert patient.age == 75


def test_is_sick() -> None:
    """Test patient is_sick."""
    connection = sqlite3.connect("test_is_sick_database.db")
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

    cursor.executemany(
        "INSERT INTO patients Values(?, ?, ?, ?, ?, ?, ?)",
        [
            (
                "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
                "Male",
                "1947-12-28 02:45:40.547",
                "Unknown",
                "Married",
                "Icelandic",
                "18.08",
            )
        ],
    )

    cursor.executemany(
        "INSERT INTO labs Values(?, ?, ?, ?, ?, ?, ?)",
        [
            (
                "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
                "1",
                "URINALYSIS: RED BLOOD CELLS",
                "1.8",
                "rbc/hpf",
                "1992-07-01 01:36:17.910",
                "0",
            )
        ],
    )
    connection.commit()
    lab_1 = Lab("FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "0")
    patient = Patient("FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", [lab_1])

    assert not patient.is_sick(
        "URINALYSIS: RED BLOOD CELLS",
        ">",
        4.0,
    )
    assert patient.is_sick(
        "URINALYSIS: RED BLOOD CELLS",
        "<",
        4.0,
    )


def test_patient_initial_age() -> None:
    """Test patient initial age."""
    connection = sqlite3.connect("test_initial_age_database.db")
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

    cursor.executemany(
        "INSERT INTO patients Values(?, ?, ?, ?, ?, ?, ?)",
        [
            (
                "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
                "Male",
                "1947-12-28 02:45:40.547",
                "Unknown",
                "Married",
                "Icelandic",
                "18.08",
            )
        ],
    )

    cursor.executemany(
        "INSERT INTO labs Values(?, ?, ?, ?, ?, ?, ?)",
        [
            (
                "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
                "1",
                "URINALYSIS: RED BLOOD CELLS",
                "1.8",
                "rbc/hpf",
                "1992-07-01 01:36:17.910",
                "0",
            )
        ],
    )
    connection.commit()
    lab_1 = Lab("FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", "0")
    patient = Patient("FB2ABB23-C9D0-4D09-8464-49BF0B982F0F", [lab_1])

    assert patient.initial_age() == 44
