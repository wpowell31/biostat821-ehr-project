"""Testing the EHR module."""
from ehr_module import parse_data
import ehr_module
from ehr_module import Lab, Patient
from fake_files import fake_files


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
        assert patient.patient_gender == "Male"
        assert patient.patient_dob == "1947-12-28 02:45:40.547"
        assert patient.patient_race == "Unknown"
        assert patient.patient_marital_status == "Married"
        assert patient.patient_language == "Icelandic"
        assert patient.patient_poverty == "18.08"


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
    ]
    with fake_files(fake_patient, fake_lab) as filenames:
        patient_records = parse_data(filenames[0], filenames[1])
        patient = patient_records[0]
        labs = patient.patient_labs
        lab = labs[0]
        assert lab.patient_id == "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F"
        assert lab.admission_id == "1"
        assert lab.lab_name == "URINALYSIS: RED BLOOD CELLS"
        assert lab.lab_value == "1.8"
        assert lab.lab_units == "rbc/hpf"
        assert lab.lab_date_time == "1992-07-01 01:36:17.910"


def test_patient_age() -> None:
    """Test patient age."""
    lab = Lab(
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "1",
        "URINALYSIS: RED BLOOD CELLS",
        "1.8",
        "rbc/hpf",
        "1992-07-01 01:36:17.910",
    )

    patient = Patient(
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "Male",
        "1947-12-28 02:45:40.547",
        "Unknown",
        "Married",
        "Icelandic",
        "18.08",
        [lab],
    )

    labs = patient.patient_labs
    lab = labs[0]
    assert patient.age == 75


def test_is_sick() -> None:
    """Test patient is_sick."""
    lab = Lab(
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "1",
        "URINALYSIS: RED BLOOD CELLS",
        "1.8",
        "rbc/hpf",
        "1992-07-01 01:36:17.910",
    )

    patient = Patient(
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "Male",
        "1947-12-28 02:45:40.547",
        "Unknown",
        "Married",
        "Icelandic",
        "18.08",
        [lab],
    )

    labs = patient.patient_labs
    lab = labs[0]
    assert patient.is_sick(
        "URINALYSIS: RED BLOOD CELLS",
        "<",
        4.0,
    )
    assert not patient.is_sick(
        "URINALYSIS: RED BLOOD CELLS",
        ">",
        4.0,
    )


def test_patient_initial_age() -> None:
    """Test patient initial age."""
    lab = Lab(
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "1",
        "URINALYSIS: RED BLOOD CELLS",
        "1.8",
        "rbc/hpf",
        "1992-07-01 01:36:17.910",
    )

    patient = Patient(
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F",
        "Male",
        "1947-12-28 02:45:40.547",
        "Unknown",
        "Married",
        "Icelandic",
        "18.08",
        [lab],
    )

    assert patient.initial_age() == 44
