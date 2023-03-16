"""Testing the EHR module."""
from ehr_module import parse_data
from ehr_module import patient_is_sick
from ehr_module import patient_age
from ehr_module import patient_initial_age
from fake_files import fake_files


def test_parse_data() -> None:
    """Test the parse data function."""
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

    fake_patient_result = {
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1947-12-28 02:45:40.547",
            "PatientRace": "Unknown",
            "PatientMaritalStatus": "Married",
            "PatientLanguage": "Icelandic",
            "PatientPopulationPercentageBelowPoverty": "18.08",
        }
    }

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
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
            "1",
            "URINALYSIS: RED BLOOD CELLS",
            "1.8",
            "rbc/hpf",
            "1992-07-01 01:36:17.910",
        ],
    ]

    fake_lab_result = {
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": [
            {
                "AdmissionID": "1",
                "LabName": "URINALYSIS: RED BLOOD CELLS",
                "LabValue": "1.8",
                "LabUnits": "rbc/hpf",
                "LabDateTime": "1992-07-01 01:36:17.910",
            }
        ]
    }

    with fake_files(fake_patient, fake_lab) as filenames:
        patient_records, lab_records = parse_data(filenames[0], filenames[1])
        assert patient_records == fake_patient_result
        assert lab_records == fake_lab_result


def test_patient_age() -> None:
    """Test patient age."""
    patient_records = {
        "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1947-12-28 02:45:40.547",
            "PatientRace": "Unknown",
            "PatientMaritalStatus": "Married",
            "PatientLanguage": "Icelandic",
            "PatientPopulationPercentageBelowPoverty": "18.08",
        }
    }
    assert (
        patient_age(patient_records, "FB2ABB23-C9D0-4D09-8464-49BF0B982F0F")
        == 75
    )


def test_patient_is_sick() -> None:
    """Test patient_is_sick."""
    fake_lab_records = {
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": [
            {
                "AdmissionID": "1",
                "LabName": "URINALYSIS: RED BLOOD CELLS",
                "LabValue": "1.8",
                "LabUnits": "rbc/hpf",
                "LabDateTime": "1992-07-01 01:36:17.910",
            }
        ]
    }
    assert patient_is_sick(
        fake_lab_records,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "URINALYSIS: RED BLOOD CELLS",
        "<",
        4.0,
    )
    assert not patient_is_sick(
        fake_lab_records,
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        "URINALYSIS: RED BLOOD CELLS",
        ">",
        4.0,
    )


def test_patient_initial_age() -> None:
    """Test patient_initial_age."""
    patient_records = {
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": {
            "PatientGender": "Male",
            "PatientDateOfBirth": "1947-12-28 02:45:40.547",
            "PatientRace": "Unknown",
            "PatientMaritalStatus": "Married",
            "PatientLanguage": "Icelandic",
            "PatientPopulationPercentageBelowPoverty": "18.08",
        }
    }
    lab_records = {
        "1A8791E3-A61C-455A-8DEE-763EB90C9B2C": [
            {
                "AdmissionID": "1",
                "LabName": "URINALYSIS: RED BLOOD CELLS",
                "LabValue": "1.8",
                "LabUnits": "rbc/hpf",
                "LabDateTime": "1992-07-01 01:36:17.910",
            }
        ]
    }
    assert (
        patient_initial_age(
            patient_records,
            lab_records,
            "1A8791E3-A61C-455A-8DEE-763EB90C9B2C",
        )
        == 44
    )
