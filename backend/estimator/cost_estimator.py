def estimate_cost(bucket_size_mb=0, selected_cols=1, total_cols=1):

    # assume scan proportional to selected columns
    scan_mb = bucket_size_mb * (selected_cols / total_cols)

    # convert MB → TB
    scan_tb = scan_mb / (1024 * 1024)

    # Athena pricing
    cost = scan_tb * 5

    return {
        "scan_bytes": round(scan_mb, 2),
        "estimated_cost": round(cost, 6)
    }