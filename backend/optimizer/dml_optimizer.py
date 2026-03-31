def analyze_dml(parsed, query):

    suggestions = []

    if not parsed.get("has_where", False):
        suggestions.append(
            "DML query without WHERE clause may affect entire dataset."
        )

    suggestions.append(
        "Athena is optimized for SELECT queries. "
        "Consider CTAS or INSERT INTO instead of UPDATE/DELETE."
    )

    return {
        "parsed": parsed,
        "optimization_score": 60,
        "risk_level": "MEDIUM",
        "suggestions": suggestions,
        "analysis": {},
        "rewrite_preview": None
    }