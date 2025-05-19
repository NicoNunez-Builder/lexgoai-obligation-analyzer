from supabase import create_client
import streamlit as st

url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["anon_key"]
supabase = create_client(url, key)

def store_obligations(data, user_email, file_name, full_text):
    for item in data:
        ob = item.get("obligation", {})
        supabase.table("obligations").insert({
            "user_email": user_email,
            "file_name": file_name,
            "obligor": ob.get("obligor"),
            "obligee": ob.get("obligee"),
            "action": ob.get("action"),
            "condition": ob.get("condition"),
            "deadline": ob.get("deadline"),
            "clause_type": ob.get("clause_type", "Unknown"),
            "risk": ob.get("risk", "Medium"),
            "clause_text": ob.get("clause_text"),
            "full_text": full_text
        }).execute()
