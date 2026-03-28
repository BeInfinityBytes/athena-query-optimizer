import sqlglot
from sqlglot import exp


def parse_query(query: str):

    tree = sqlglot.parse_one(query)

    # -------- table --------
    table_exp = tree.find(exp.Table)
    table = table_exp.name if table_exp else None

    # -------- columns --------
    columns = []
    select_exp = tree.find(exp.Select)

    for projection in select_exp.expressions:
        if isinstance(projection, exp.Star):
            columns.append("*")
        else:
            columns.append(projection.alias_or_name)

    # -------- where --------
    has_where = tree.find(exp.Where) is not None

    return {
        "table": table,
        "columns": columns,
        "has_where": has_where,
        "ast": tree
    }