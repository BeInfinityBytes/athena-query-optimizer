import sqlglot
from sqlglot import exp


def parse_query(query: str):
    """
    Safe SQL parser supporting:
    - SELECT
    - UPDATE
    - DELETE
    - INSERT
    - Invalid SQL handling
    """

    try:
        # -------------------------
        # Parse SQL safely
        # -------------------------
        tree = sqlglot.parse_one(query)

    except Exception as e:
        return {
            "valid": False,
            "error": "Invalid SQL syntax",
            "details": str(e)
        }

    # -------------------------
    # Query Type Detection
    # -------------------------
    query_type = tree.key.upper() if tree.key else "UNKNOWN"

    # -------------------------
    # Table Detection
    # -------------------------
    table_exp = tree.find(exp.Table)
    table = table_exp.name if table_exp else None

    # -------------------------
    # Column Detection (SELECT only)
    # -------------------------
    columns = []

    if query_type == "SELECT":
        select_exp = tree.find(exp.Select)

        if select_exp and select_exp.expressions:
            for projection in select_exp.expressions:

                if isinstance(projection, exp.Star):
                    columns.append("*")

                else:
                    columns.append(projection.alias_or_name)

    # -------------------------
    # WHERE Detection
    # -------------------------
    has_where = tree.find(exp.Where) is not None

    # -------------------------
    # Return Structured Output
    # -------------------------
    return {
        "valid": True,
        "query_type": query_type,
        "table": table,
        "columns": columns,
        "has_where": has_where,
        "ast": tree
    }