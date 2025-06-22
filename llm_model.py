import os
os.environ.pop("SSL_CERT_FILE", None)  # 🔧 fix Groq SSL crash
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


def load_data():
    with open("output.json", "r") as f:
        return json.load(f)

# LangChain Expression Language Prompt
prompt_template = ChatPromptTemplate.from_template("""
You are an AI assistant summarizing official company filings.

Based on the Form ADT-1 data below, generate a 3–5 line summary in plain English suitable for a non-technical person:

- Company Name: {company_name}
- CIN: {cin}
- Registered Office: {registered_office}
- Appointment Date: {appointment_date}
- Auditor Name: {auditor_name}
- Auditor Address: {auditor_address}
- FRN/Membership: {auditor_frn_or_membership}
- Appointment Type: {appointment_type}

Summary:
""")

# Create LLM instance
llm = ChatGroq(
    model_name="llama3-70b-8192",
    temperature=0.2,
)

# Create LCEL runnable
chain = prompt_template | llm

def main():
    data = load_data()
    response = chain.invoke(data)
    summary = response.content.strip()

    with open("summary.txt", "w") as f:
        f.write(summary)

    print("✅ AI summary saved to summary.txt")

if __name__ == "__main__":
    main()
