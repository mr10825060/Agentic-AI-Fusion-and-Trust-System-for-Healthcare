from langchain_openai import ChatOpenAI

#Create LLM 
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="6v3Ss3_xvOoJalRDdkGLbiKP9-skjD4KiWMLwJJ351wJ8DRwJk5R7J4vbzUA"
)

#Main Function
def llm_agent(question, context):

    prompt = f"""
You are a healthcare data assistant.

You have access to structured hospital data:

INSIGHTS:
{context.get("insights")}

DATA COLUMNS:
{context.get("columns")}

SAMPLE DATA:
{context.get("fused_sample")}

RULES:
- If user asks about "patients", use sample data
- If user asks "top diseases", use insights or sample
- If data is missing, clearly say so
- Be short and accurate

QUESTION:
{question}
"""

    response = llm.invoke(prompt)
    return response.content