import streamlit as st
import matplotlib.pyplot as plt

from graph import build_graph
from agents.llm_agent import llm_agent

st.title("Agentic AI Fusion and Trust System")

# ---------------- BUILD PIPELINE ----------------
graph = build_graph()

# ---------------- SESSION STATE ----------------
if "result" not in st.session_state:
    st.session_state.result = None

if "insights" not in st.session_state:
    st.session_state.insights = {}

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- RUN SYSTEM ----------------
if st.button("Run System"):

    result = graph.invoke({})

    st.session_state.result = result
    st.session_state.insights = result.get("insights", {})

    st.success("System executed successfully!")

# ---------------- LOAD DATA ----------------
result = st.session_state.result
insights = st.session_state.insights

# ---------------- SHOW OUTPUT ----------------
if result:

    fused = result.get("fused", None)
    trust_scores = result.get("trust_scores", {})
    overall = result.get("overall_trust", 0)

    # ---------------- INSIGHTS ----------------
    st.subheader("Insights")
    st.json(insights)

    # ---------------- FUSED DATA ----------------
    st.subheader("Fused Healthcare Data")

    if fused is not None:
        st.write("Total Rows:", len(fused))
        st.write("Total Patients:", fused["subject_id"].nunique())
        st.dataframe(fused, width="stretch")
    else:
        st.warning("No fused data available")

    # ---------------- TRUST ----------------
    st.subheader("Trust Scores")
    st.write(trust_scores)
    st.metric("Overall Trust Score", overall)

    # ---------------- TRUST ANALYSIS (ONLY PIE CHART) ----------------
    st.subheader("Trust Analysis")

    if trust_scores:

        fig2, ax2 = plt.subplots()
        ax2.pie(
            trust_scores.values(),
            labels=trust_scores.keys(),
            autopct="%1.1f%%"
        )
        st.pyplot(fig2)

    else:
        st.warning("No trust scores available")

    # ---------------- DATA QUALITY ----------------
    st.subheader("Data Quality Analysis")

    if fused is not None:
        missing = fused.isnull().sum().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots()
        ax.bar(missing.index, missing.values)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # ---------------- PATIENT TIMELINE ----------------
    st.subheader("Patient Timeline")

    if fused is not None and "subject_id" in fused.columns:

        patient_ids = fused["subject_id"].dropna().unique()
        selected_patient = st.selectbox("Select Patient ID", patient_ids)

        patient_data = fused[fused["subject_id"] == selected_patient]

        st.dataframe(patient_data, width="stretch")

        if "admittime" in patient_data.columns:

            timeline = patient_data.sort_values("admittime")

            fig, ax = plt.subplots()
            ax.plot(range(len(timeline)), timeline["admittime"])
            plt.xticks(rotation=45)
            st.pyplot(fig)

    else:
        st.warning("Patient timeline not available")

    # ---------------- CHATGPT STYLE AI ASSISTANT ----------------
    st.subheader("AI Assistant (ChatGPT Style)")

    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f"🧑‍💻 **You:** {msg['content']}")
        else:
            st.markdown(f"🤖 **AI:** {msg['content']}")

    user_input = st.text_input("Type your message here")

    if st.button("Send") and user_input:

        st.session_state.chat.append({
            "role": "user",
            "content": user_input
        })

        # ✅ FIXED CONTEXT (IMPORTANT)
        context = {
            "insights": insights,
            "fused_sample": fused.head(10).to_dict() if fused is not None else {},
            "columns": list(fused.columns) if fused is not None else []
        }

        response = llm_agent(user_input, context)

        st.session_state.chat.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()