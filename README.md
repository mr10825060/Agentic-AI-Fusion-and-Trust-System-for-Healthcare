# 🏥 Agentic AI Data Fusion and Trust System

##  Brief One-Line Summary
A multi-agent healthcare intelligence system that fuses fragmented clinical data from MIMIC-IV into a unified record with automated trust scoring and a conversational AI assistant.[cite: 1]

---

## Overview
This project implements the **Agentic AI Fusion and Trust System (AAFTS)**, a novel framework designed to overcome healthcare data fragmentation. By orchestrating specialized AI agents via **LangGraph**, the system integrates heterogeneous clinical data streams—such as lab results, medications, and diagnoses—into a single, actionable patient-level representation.

The system was validated using the **MIMIC-IV Demo Dataset**, processing records for **100 de-identified patients** across 128 hospitalizations.

---

##  Problem Statement
Modern healthcare data is often trapped in isolated silos, leading to:
*   **Data Fragmentation**: Patient info is split across demographics, labs, and pharmacy systems.
*   **No Trust Evaluation**: Lack of mechanisms to quantify the reliability or completeness of a patient record.
*   **Limited Interpretability**: AI clinical outputs often lack confidence scores or explainability.
*   **Complex Access**: Clinicians must use complex queries instead of natural language to extract insights.

---

##  Dataset
*   **Source**: MIMIC-IV Demo Dataset (PhysioNet).
*   **Scope**: 100 patients, 128 admissions, 5,706 lab measurements, and 4,156 prescriptions.
*   **Key Tables**:
    *   `patients.csv`: Core demographics.
    *   `admissions.csv`: Hospital visit records.
    *   `labevents.csv`: Laboratory measurements.
    *   `prescriptions.csv`: Medication orders.
    *   `diagnoses_icd.csv`: Clinical diagnosis codes.

---

##  Tools and Technologies
*   **Orchestration**: LangGraph, LangChain.
*   **LLM Backend**: OpenAI GPT-4o / GPT-4o-mini.
*   **Processing**: Python, Pandas, NumPy.
*   **Interface**: Streamlit (Interactive Dashboard).
*   **Visualization**: Plotly, Matplotlib.

---

##  Methods
*   **Multi-Agent Pipeline**: A sequential five-stage workflow: **Ingestion → Cleaning → Fusion → Analysis → Trust Scoring**.
*   **Data Fusion**: Hierarchical merging using `subject_id` and `hadm_id` to create a unified clinical view.
*   **Composite Trust Scoring**: A system quantifying data reliability based on completeness and missing value ratios.
*   **Conversational RAG**: A ChatGPT-style interface grounded in fused clinical data to answer natural language queries.

---

##  Key Insights
*   **100% Pipeline Success**: The agentic workflow successfully automated the transition from raw CSVs to fused insights.
*   **Unified Representation**: Successfully merged 5+ independent tables into a single hospitalization record.
*   **Trust Calibration**: Identified data quality variations; while the demo data scored high (1.0), the system is built to flag low-trust records for clinical review.
*   **Efficiency**: The AI assistant provides context-aware responses with an average latency of **1.8 seconds**.

---

##  Dashboard / Output
*   **Unified Clinical Table**: A searchable view of merged patient demographics, labs, and diagnoses.
*   **Trust Analysis**: Visualizations (pie and bar charts) showing data quality across different clinical domains.
*   **Patient Timeline**: Interactive plots of hospital admissions over time.
*   **Conversational AI**: A chat interface for querying "total patients," "top diseases," or specific patient details.

---

##  How to Run This Project

### Step 1: Clone the repository
```bash
git clone https://github.com/your-username/agentic-health-fusion.git
cd agentic-health-fusion
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set up environment variables
Create a `.env` file and add your OpenAI API Key:
```bash
OPENAI_API_KEY=your_api_key_here( due to Privacy I remove that)
```

### Step 4: Launch the dashboard
```bash
streamlit run app.py
```
