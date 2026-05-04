def analysis_agent(data):

    insights = {}

    # Total patients
    if "patients" in data:
        insights["total_patients"] = len(data["patients"])

    # Total admissions
    if "admissions" in data:
        insights["total_admissions"] = len(data["admissions"])

    # Total diagnoses
    if "diagnoses" in data:
        insights["total_diagnoses"] = len(data["diagnoses"])

    # Total prescriptions
    if "prescriptions" in data:
        insights["total_prescriptions"] = len(data["prescriptions"])

    # Total procedures
    if "procedures" in data:
        insights["total_procedures"] = len(data["procedures"])

    # Total lab records
    if "labs" in data:
        insights["total_labs"] = len(data["labs"])

    return insights