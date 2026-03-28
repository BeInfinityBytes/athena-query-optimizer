from sqlglot import exp


def generate_suggestions(parsed, schema):

    suggestions = []

    selected_columns = parsed["columns"]
    has_where = parsed["has_where"]
    ast = parsed["ast"]

    schema_columns = [c.lower() for c in schema]

    # -----------------------------------
    # Rule 1 — SELECT *
    # -----------------------------------
    if "*" in selected_columns:
        suggestions.append(
            "Avoid SELECT *. Scan only required columns."
        )

    # -----------------------------------
    # Rule 2 — Full table scan
    # -----------------------------------
    if not has_where:
        suggestions.append(
            "Query performs full table scan. Add filters."
        )

    # -----------------------------------
    # Rule 3 — Partition pruning detection
    # -----------------------------------
    partition_candidates = [
        c for c in schema_columns
        if any(k in c for k in ["year", "date", "month", "day"])
    ]

    if partition_candidates:

        if has_where:
            where_clause = ast.find(exp.Where)

            if where_clause:
                where_sql = where_clause.sql().lower()

                for p in partition_candidates:
                    if p not in where_sql:
                        suggestions.append(
                            f"Consider filtering on partition column '{p}'."
                        )
        else:
            for p in partition_candidates:
                suggestions.append(
                    f"Filtering using '{p}' can significantly reduce scan cost."
                )

    # Remove duplicates
    return list(set(suggestions))