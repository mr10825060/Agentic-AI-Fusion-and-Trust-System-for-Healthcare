import pandas as pd

def ingestion_agent():
    data = {}

    files = {
        "patients": "patients.csv",
        "admissions": "admissions.csv",
        "labs": "labevents.csv",
        "prescriptions": "prescriptions.csv",
        "diagnoses": "diagnoses_icd.csv",
        "procedures": "procedures_icd.csv",
        "diag_lookup": "d_icd_diagnoses.csv"
    }

    for key, file in files.items():
        data[key] = pd.read_csv(f"data/{file}")

    return data