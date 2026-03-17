from fastapi import FastAPI
from pydantic import BaseModel
from parser.sql_parser import parse_query
from optimizer.rules import detect_select_star, check_no_where
from estimator.cost_estimator import estimate_cost



app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.get("/")
def home():
    return {"message": "Athena Query Optimizer Running "}


@app.post("/analyze")
def analyze_query(data: QueryInput):

    parsed = parse_query(data.query)

    warnings = []

    cost = estimate_cost()

    if detect_select_star(parsed["columns"]):
        warnings.append("Avoid using SELECT *")

    if check_no_where(data.query):
        warnings.append("Query has no WHERE clause (full scan risk)")

    return {
        "parsed": parsed,
        "warnings": warnings,
        "cost estimate":cost
    }