from optimizer.suggestions import generate_suggestions
from optimizer.scorer import calculate_score
from optimizer.advanced_analysis import analyze_query_efficiency
from optimizer.rewrite_engine import generate_rewrite
from optimizer.dml_optimizer import analyze_dml


def route_optimizer(parsed, schema, query, cost):

    # ---------------- INVALID SQL ----------------
    if not parsed.get("valid", True):
        return {
            "status": "error",
            "message": parsed.get(
                "error",
                "Invalid SQL query."
            )
        }

    query_type = parsed.get("query_type", "SELECT")

    # ---------------- SELECT ----------------
    if query_type == "SELECT":

        suggestions = generate_suggestions(parsed, schema)

        score, risk = calculate_score(suggestions)

        analysis = analyze_query_efficiency(parsed, schema)

        rewrite_preview = generate_rewrite(
            parsed,
            schema,
            query
        )

        return {
            "parsed": parsed,
            "estimated_cost": cost,
            "optimization_score": score,
            "risk_level": risk,
            "suggestions": suggestions,
            "analysis": analysis,
            "rewrite_preview": rewrite_preview
        }

    # ---------------- DML ----------------
    elif query_type in ["UPDATE", "DELETE", "INSERT"]:
        return analyze_dml(parsed, query)

    # ---------------- OTHER ----------------
    else:
        return {
            "status": "info",
            "message": f"{query_type} queries are not yet supported."
        }