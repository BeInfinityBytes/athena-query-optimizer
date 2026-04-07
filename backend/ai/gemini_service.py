from google import genai
from config import GEMINI_API_KEY
import logging

# Ensure the model client is configured using the new google-genai SDK
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None
    
# Updated to use flash-lite-latest per your request
MODEL_NAME = 'gemini-flash-lite-latest'

def generate_optimization_explanation(old_query: str, optimized_query: str, schema: list = None) -> str:
    """
    Calls Gemini API to explain the optimizations made to the query.
    """
    if not client:
        return "Gemini API is not configured or failed to initialize."
        
    prompt = f"""
You are an expert Data Engineer and Amazon Athena query optimizer. 
Explain to a Data Analyst why the 'Optimized SQL' is more cost-effective and faster in Amazon Athena than the 'Original SQL'. 
Keep it concise, clear, and focused on Athena specific optimizations (like partitions, columnar formats, reducing data scanned).

Original SQL:
```sql
{old_query}
```

Optimized SQL:
```sql
{optimized_query}
```

Schema columns for context: {schema if schema else 'Not provided'}

Provide your explanation in a brief, easy-to-read markdown format. Do not repeat the queries.
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
    except Exception as e:
        logging.error(f"Gemini API Error: {e}")
        return "Explanation could not be generated at this time."

def generate_complex_rewrite(query: str, schema: list) -> str:
    """
    Experimental: Uses Gemini to attempt a complex rewrite when rule-based parser fails.
    """
    if not client:
        return query
        
    prompt = f"""
You are an expert Data Engineer and Amazon Athena Database Admin. 
Rewrite the following SQL query to be highly optimized for Amazon Athena.
Apply techniques such as partition pruning, specific column selection instead of *, and replacing inefficient joins.

Original SQL:
```sql
{query}
```

Available Schema Columns: {schema}

Only return the optimized SQL query code, nothing else. No formatting blocks, just the code.
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        # Strip potential markdown code blocks from response
        text = response.text.replace("```sql", "").replace("```", "").strip()
        return text
    except Exception as e:
        logging.error(f"Gemini API Error: {e}")
        return query
