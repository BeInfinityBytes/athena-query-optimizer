# import sqlparse


# def parse_query(query: str):

#     query = query.lower()

#     columns_part = query.split("from")[0].replace("select", "").strip()
#     table_part = query.split("from")[1].strip()

#     columns = [c.strip() for c in columns_part.split(",")]

#     # ✅ REMOVE semicolon + spaces
#     table = table_part.replace(";", "").strip()

#     return {
#         "columns": columns,
#         "table": table
#     }

import re

def clean_identifier(name: str):
    return re.sub(r"[;]", "", name).strip()

def parse_query(query: str):

    query = query.lower()

    columns_part = query.split("from")[0].replace("select", "").strip()
    table_part = query.split("from")[1]

    columns = [c.strip() for c in columns_part.split(",")]
    table = clean_identifier(table_part)

    return {
        "columns": columns,
        "table": table
    }