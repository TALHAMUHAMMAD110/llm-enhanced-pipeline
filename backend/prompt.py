from schema import sales_schema

def query_prompt(user_query: str) -> str:
    
    prompt = f"""
    You are an expert PostgreSQL developer. Your task is to translate a user's business logic into a precise and executable PostgreSQL query based on the provided database schema.
    
    our sales table has the following structure:
     - id: SERIAL PRIMARY KEY
     - document_id: INT NOT NULL
     - raw_text: TEXT
     - invoice_number: VARCHAR(100)
     - shop: VARCHAR(100)
     - total: NUMERIC(12, 2)
     - currency: VARCHAR(10)
     - timestamp: TIMESTAMP
     - item: VARCHAR(255)
     - price: NUMERIC(12, 2)

    **Instructions:**
    1.  Analyze the database schema below to understand the table structures, columns, and relationships.
    2.  Read the user's business logic carefully.
    3.  Generate a single, clean, and correct PostgreSQL query that fulfills the user's request with no "\n" please.
    4.  Do not include any explanations, comments, or markdown formatting in your response. Only output the raw SQL query.


    **User's Business Logic:**
    "{user_query}"

    **Generated PostgreSQL Query:**
    """
    
    return prompt