def estimate_clause_risk(action_text):
    keywords = ["indemnify", "terminate", "liable", "confidential", "breach"]
    score = sum(1 for k in keywords if k in action_text.lower())
    if score >= 2:
        return "High"
    elif score == 1:
        return "Medium"
    else:
        return "Low"
