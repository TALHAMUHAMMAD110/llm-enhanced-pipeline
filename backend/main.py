
from fastapi import FastAPI, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db
from google import genai
import os
from prompt import query_prompt


app = FastAPI()


@app.get("/shops")
async def get_shops(db: AsyncSession = Depends(get_db)):
    
    query = 'SELECT distinct shop FROM sales;'
    result = await db.execute(text(query))
    
    shops = result.scalars().all()
    
    return {
        "shops": shops
    }

@app.get("/generate_query")
async def generate_query(
    query: str = Query(..., description="SQL query to execute"),
    db: AsyncSession = Depends(get_db)
):
    
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=query_prompt(query),
    )

    return {
        "user_prompt": query,
        "generated_query": response.text.strip()
    }