from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text
from database import engine

app = FastAPI(title="ElectriSeati API")



@app.get("/health")
async def healthcheck():
     async with engine.connect() as connection:
          result = await connection.execute(text("SELECT 1"))
          return {"status":"ok","database":result.scalar()}



class CategoryCreate(BaseModel):
    name: str

@app.get("/categories")
async def GetCategories():
     async with engine.connect() as connection:
          result = await connection.execute(

               text("SELECT id ,name FROM categories ORDER BY id")
          )
          categories =[
              {

               "id":row.id,
               "name":row.name,
              }
              for row in result

          ]

          return {

               "categories":categories
          }


@app.post("/categories")
async def create_category(category: CategoryCreate):
    async with engine.begin() as connection:
        result = await connection.execute(
            text(
                "INSERT INTO categories (name) "
                "VALUES (:name) "
                "RETURNING id, name"
            ),
            {"name": category.name},
        )

        new_category = result.fetchone()

        return {
            "id": new_category.id,
            "name": new_category.name,
        }