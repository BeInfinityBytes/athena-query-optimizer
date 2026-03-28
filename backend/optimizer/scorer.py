def calculate_score(suggestions):

    score = 100

    if any("SELECT *" in s for s in suggestions):
        score -= 30

    if any("WHERE" in s for s in suggestions):
        score -= 25

    if any("partition" in s.lower() for s in suggestions):
        score -= 20

    if any("many columns" in s.lower() for s in suggestions):
        score -= 15

    score = max(score, 10)   # never show 0 (better UX)

    if score > 75:
        risk = "LOW"
    elif score > 40:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return score, risk