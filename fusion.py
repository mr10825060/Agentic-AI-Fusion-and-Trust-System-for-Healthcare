import pandas as pd

def fusion_agent(data):

    patients = data.get("patients")
    admissions = data.get("admissions")
    diagnoses = data.get("diagnoses")
    prescriptions = data.get("prescriptions")
    procedures = data.get("procedures")
    labs = data.get("labs")
    diag_lookup = data.get("diag_lookup")

    # ---------------- STEP 1: patients + admissions ----------------
    df = patients.merge(admissions, on="subject_id", how="left")

    # ---------------- STEP 2: diagnoses ----------------
    if diagnoses is not None:

        # merge lookup BEFORE aggregation
        if diag_lookup is not None and \
           "icd_code" in diagnoses.columns and \
           "icd_version" in diagnoses.columns:

            diagnoses = diagnoses.merge(
                diag_lookup,
                on=["icd_code", "icd_version"],
                how="left"
            )

        # diagnosis names
        if "long_title" in diagnoses.columns:
            diag_clean = diagnoses.groupby(
                ["subject_id", "hadm_id"]
            )["long_title"].apply(
                lambda x: ", ".join(x.dropna().astype(str).unique())
            ).reset_index()

            diag_clean.rename(columns={"long_title": "diagnoses_list"}, inplace=True)

            df = df.merge(diag_clean, on=["subject_id", "hadm_id"], how="left")

        # ICD codes
        if "icd_code" in diagnoses.columns:
            diag_codes = diagnoses.groupby(
                ["subject_id", "hadm_id"]
            )["icd_code"].apply(
                lambda x: ", ".join(x.dropna().astype(str).unique())
            ).reset_index()

            df = df.merge(diag_codes, on=["subject_id", "hadm_id"], how="left")

        # top diseases
        if "long_title" in diagnoses.columns:
            top_diseases = diagnoses["long_title"].value_counts().head(10).to_dict()
            df["top_diseases_summary"] = str(top_diseases)

    # ---------------- STEP 3: prescriptions ----------------
    if prescriptions is not None and "drug" in prescriptions.columns:
        pres_agg = prescriptions.groupby(
            ["subject_id", "hadm_id"]
        )["drug"].apply(
            lambda x: ", ".join(x.dropna().astype(str).unique())
        ).reset_index()

        df = df.merge(pres_agg, on=["subject_id", "hadm_id"], how="left")

    # ---------------- STEP 4: procedures ----------------
    def get_icd_col(df_):
        if df_ is None:
            return None
        if "icd_code" in df_.columns:
            return "icd_code"
        if "icd9_code" in df_.columns:
            return "icd9_code"
        return None

    if procedures is not None:
        proc_col = get_icd_col(procedures)

        if proc_col:
            proc_agg = procedures.groupby(
                ["subject_id", "hadm_id"]
            )[proc_col].apply(
                lambda x: ", ".join(x.dropna().astype(str).unique())
            ).reset_index()

            df = df.merge(proc_agg, on=["subject_id", "hadm_id"], how="left")

    # ---------------- STEP 5: labs ----------------
    if labs is not None and "valuenum" in labs.columns:
        lab_agg = labs.groupby(
            ["subject_id", "hadm_id"]
        )["valuenum"].mean().reset_index()

        lab_agg.rename(columns={"valuenum": "avg_lab_value"}, inplace=True)

        df = df.merge(lab_agg, on=["subject_id", "hadm_id"], how="left")

    # ---------------- FINAL CLEAN (NO WARNINGS FIX) ----------------

    def make_safe(val):
        if isinstance(val, list):
            return ", ".join(map(str, val))
        if isinstance(val, dict):
            return str(val)
        return val

    # FIX: replace deprecated applymap
    df = df.astype(object).apply(lambda col: col.map(make_safe))

    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True)

    return df