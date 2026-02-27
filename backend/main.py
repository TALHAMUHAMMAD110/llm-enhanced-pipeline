from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from models import Sale

app = FastAPI()


@app.get("/shops")
async def get_shops(db: AsyncSession = Depends(get_db)):
    
    query = select(Sale.shop)
    result = await db.execute(query)
    
    shops = result.scalars().all()
    
    return {
        "shops": shops
    }