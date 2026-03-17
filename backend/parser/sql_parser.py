import sqlparse

def parse_query(query: str):
    query = query.lower()

    table = None
    columns = []
    
    if "from" in query:
        table = query.split("from")[1].split()[0]

    if "select" in query:
        cols = query.split("from")[0].replace("select", "").strip()
        columns = [c.strip() for c in cols.split(",")]

    return {
        "table": table,
        "columns": columns
    }