from fastapi import FastAPI
from pydantic import BaseModel
from parser.sql_parser import parse_query
from optimizer.rules import detect_select_star, check_no_where
from estimator.cost_estimator import estimate_cost
from aws.glue_service import get_table_schema
from aws.s3_service import get_bucket_size



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

@app.get("/schema")
def schema():
    cols = get_table_schema("optimizer_db", "sales")
    return {"columns": cols}

@app.post("/optimize")
def optimize(data: QueryInput):

    parsed = parse_query(data.query)

    schema = get_table_schema("optimizer_db", parsed["table"])

    size = get_bucket_size("athena-query-optimizer-data")

    cost = estimate_cost(
        size,
        len(parsed["columns"]),
        len(schema)
    )

    return {
        "parsed": parsed,
        "estimated_cost": cost
    }