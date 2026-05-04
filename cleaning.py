def cleaning_agent(data):

    cleaned_data = {}

    for name, df in data.items():

        # Make a copy (important to avoid modifying original data)
        df = df.copy()

        # ---------------- HANDLE MISSING VALUES ----------------
        df = df.ffill()   # forward fill (fixes your warning)

        # ---------------- REMOVE DUPLICATES ----------------
        df = df.drop_duplicates()

        # ---------------- STANDARDIZE COLUMN NAMES ----------------
        df.columns = [col.strip().lower() for col in df.columns]

        # ---------------- OPTIONAL: STRIP STRING VALUES ----------------
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()

        # Save cleaned dataset
        cleaned_data[name] = df

    return cleaned_data