def detect_select_star(columns):
    return "*" in columns

def check_no_where(query):
    return "where" not in query.lower()