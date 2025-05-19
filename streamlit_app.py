import streamlit as st
import pandas as pd
import json
from utils.db import store_obligations
from utils.risk_scoring import estimate_clause_risk
from utils.clause_parser import split_into_clauses

st.set_page_config(layout="wide", page_title="LexGoAI Legal Obligation Analyzer")

st.title("LexGoAI Legal Obligation Analyzer")

uploaded_file = st.file_uploader("Upload a contract (.pdf, .docx, or .txt)", type=["pdf", "docx", "txt"])

if uploaded_file:
    file_name = uploaded_file.name

    def read_uploaded_file(file):
        if file.name.endswith(".pdf"):
            from pdfminer.high_level import extract_text
            return extract_text(file)
        elif file.name.endswith(".docx"):
            from docx import Document
            return "\n".join([p.text for p in Document(file).paragraphs])
        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")
        else:
            return None

    contract_text = read_uploaded_file(uploaded_file)
    clauses = split_into_clauses(contract_text)

    obligations = []
    for clause in clauses:
        obligations.append({
            "obligation": {
                "obligor": "Party A",
                "obligee": "Party B",
                "action": clause[:50] + "...",
                "condition": "If applicable",
                "deadline": "30 days",
                "clause_type": "Obligation",
                "risk": estimate_clause_risk(clause),
                "clause_text": clause
            }
        })

    email = st.text_input("Enter your email to store the data:")
    if email and st.button("Store to Supabase"):
        store_obligations(obligations, email, file_name, contract_text)
        st.success("Data stored successfully.")

    st.subheader("Extracted Obligations")
    df = pd.DataFrame([o["obligation"] for o in obligations])
    st.dataframe(df)
