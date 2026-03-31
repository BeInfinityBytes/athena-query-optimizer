def generate_rewrite(parsed, schema, original_query):

    table = parsed["table"]
    columns = parsed["columns"]
    has_where = parsed["has_where"]

    # -----------------------------
    # Detect already optimized query
    # -----------------------------
    if "*" not in columns and has_where:
        # Already good → don't modify
        return original_query.strip()

    # -----------------------------
    # Fix SELECT *
    # -----------------------------
    if "*" in columns:
        preview_cols = schema[:3]
    else:
        preview_cols = columns

    column_sql = ", ".join(preview_cols)

    query = f"SELECT {column_sql} FROM {table}"

    # -----------------------------
    # Add partition suggestion ONLY if missing
    # -----------------------------
    partition_cols = [
        c for c in schema
        if any(k in c.lower() for k in ["year", "date", "month"])
    ]

    if not has_where and partition_cols:
        query += f" WHERE {partition_cols[0]} = ?"

    return query