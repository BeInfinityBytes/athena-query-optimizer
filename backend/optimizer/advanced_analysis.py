def analyze_query_efficiency(parsed, schema):

    total_columns = len(schema)

    selected_columns = parsed["columns"]

    # SELECT * case
    if "*" in selected_columns:
        selected_count = total_columns
    else:
        selected_count = len(selected_columns)

    efficiency = round(
        (1 - (selected_count / total_columns)) * 100, 2
    )

    return {
        "total_columns": total_columns,
        "selected_columns": selected_count,
        "scan_efficiency": f"{efficiency}%"
    }