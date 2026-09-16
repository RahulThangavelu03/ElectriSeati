from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI(title="ElectriSeati API")



@app.get("/health")
async def healthcheck():
     async with engine.connect() as connection:
          result = await connection.execute(text("SELECT 1"))
          return {"status":"ok","database":result.scalar()}

