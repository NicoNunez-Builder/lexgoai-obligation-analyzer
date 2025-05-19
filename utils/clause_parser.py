# Placeholder for clause parsing logic
def split_into_clauses(text, min_length=30):
    return [clause.strip() for clause in text.split("\n") if len(clause.strip()) > min_length]
