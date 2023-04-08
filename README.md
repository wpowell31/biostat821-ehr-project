# ehr-utils

The ehr-utils library provides some simple analytical capabilities for EHR data.

# End User Documentation

## Setup/Installation instructions

To use this software, you will need to have Python 3.6 or later installed on your system. You can download Python from the official website: https://www.python.org/downloads/

## Input File Formats
The module accepts data in the form of .txt files. The data are in the form of
    Table 1: Patient Demographic Data    
    Table 2: Labratory Results

All input file should be tab sebarated, with string values not in quotes. For the Patient Demographic Data file, every entry is for a unique patient. For the Labratory Results file, the same patient can have multiple labs, and multiple labs for the same admission. The first line for both files should be a header that gives the column names for the fields in the file. An arbitrary number of headers can be supported, however typical column names for the patient demographic file are PatientID, PatientGender, PatientDateOfBirth, PatientRace, PatientMaritalStatus, PatientLanguage, and PatientPopulationPercentageBelowPoverty. For the labratory results file the typical headers are PatientID, AdmissionID, LabName, LabValue, LabUnits, and LabDateTime.

## API
Data are stored in classes, with:
    a Patient class with:
    instance attributes for gender, DOB, race, poverty status, language, marital status, and labs.

    a Lab class with:
    instance attributes for name, value, units, admissionID, and date.

Each instance of a patient class includes each lab stored in a list of lab classes.

Old patients
The function age(self) -> int: takes the data and returns the age in years of the given patient. For example,

>> patient.age
49


Sick patients
The method is_sick(self, lab_name: str, operator: str, value: float) -> bool: takes the data and returns a boolean indicating whether the patient has ever had a test with value above (">") or below ("<") the given level. For example,

>> patient.is_sick("METABOLIC: ALBUMIN", ">", 4.0)
True

Age at first admission
The method initial_age(self) -> int: takes in the patient records, lab records, and patient id string and returns the age of that patient whenever their earliest lab was recorded. For example,

>> patient.initial_age()
44

# Contributor Instructions

To test the data, run sets using the pytest library. To do so, navigate to the working directory and run pytest.
To test for coverage, run pytest --cov=ehr_module tests/. 


