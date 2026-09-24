from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import text
from database import engine

from datetime import datetime

from app.models.event_type import EventType
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError

app = FastAPI(title="ElectriSeati API")


class CreateEvent(BaseModel):
    title: str
    description: str | None = None
    event_type: EventType
    category_id: int
    venue_id: int
    starts_at: datetime



class CreateVenue(BaseModel):

    name:str
    location:str



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



@app.post("/events")

async def Create_Events(event:CreateEvent):
    async with engine.begin() as connection:
        
        result= await connection.execute(

           text("""
            
            SELECT id FROM categories WHERE id = :category_id
           
           
           
           """),

              {"category_id":event.category_id}


        )
        category = result.fetchone()

        if category is None:
           raise HTTPException(
           status_code=404,
           detail="Category not found"
        )

        result = await connection.execute(

            text("""
            
              SELECT id FROM venues WHERE id = :venue_id
             
            
             """),
                { "venue_id":event.venue_id } 

        )
        

        venue_data = result.fetchone()

        if venue_data is None:
             raise HTTPException(
           status_code=404,
           detail="Venue not found"
        )



     

        result= await connection.execute(

            text("""
            INSERT INTO events (title,description,event_type,category_id,venue_id,starts_at,created_at)
            
            VALUES
             (:title, :description ,:event_type, :category_id, :venue_id, :starts_at,NOW())
             RETURNING id, title, description, event_type, category_id , venue_id,starts_at,created_at
            
            
            """),

            {
               "title":event.title,
               "description":event.description,
               "event_type":event.event_type.value,
               "category_id":event.category_id,
               "venue_id":event.venue_id,
               "starts_at":event.starts_at,
               



            }
        )
        
        new_event= result.fetchone()

        return {

           "id":new_event.id,
           "title":new_event.title,
           "description":new_event.description,
           "event_type":new_event.event_type,
           "category_id":new_event.category_id,
           "venue_id":new_event.venue_id,
           "starts_at":new_event.starts_at,
           "created_at":new_event.created_at,

        }


@app.get("/events")
async def get_events():

    async with engine.connect() as connection:

        result = await connection.execute(

            text( """
            
            
            
            SELECT id,title,description,event_type,category_id,venue_id,starts_at,created_at FROM events ORDER BY id
            
            
            
            
            
             """)
        )

        events = [

            {
               
                "id":row.id,
                "title":row.title,
                "description":row.description,
                "event_type":row.event_type,
                "category_id":row.category_id,
                "venue_id":row.venue_id,
                "starts_at":row.starts_at,
                "created_at":row.created_at,



            }

            for row in result
        ]

        return {

             "events":events
        }
         

@app.get("/events/{event_id}")
async def get_event(event_id: int):

    async with engine.connect() as connection:

        result = await connection.execute(
            text(
                """
                SELECT
                    id,
                    title,
                    description,
                    event_type,
                    category_id,
                    venue,
                    starts_at,
                    created_at
                FROM events
                WHERE id = :event_id
                """
            ),
            {"event_id": event_id}
        )

        event = result.fetchone()

       
        if event is None:
           raise HTTPException(
                status_code=404,
                detail="Event not found"
          )    

  
        return {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "event_type": event.event_type,
            "category_id": event.category_id,
            "venue": event.venue,
            "starts_at": event.starts_at,
            "created_at": event.created_at,
        }



@app.put("/events/{event_id}")
async def update_event(event_id:int,event:CreateEvent):
    async with engine.begin() as connection:

         # Check if event exsist

        result = await connection.execute(

           text( """

                SELECT id FROM events WHERE id = :event_id



           """),

              { "event_id":event_id}

       

        )

        exsisting_event = result.fetchone()

        if exsisting_event is None:
           raise HTTPException(
                status_code= 404,
                detail="Event not found"
           )


        result= await connection.execute(

            text("""
            
                SELECT id FROM categories WHERE id =:category_id
            
            
            
            """),

            {"category_id":event.category_id}


            )


        
        category = result.fetchone()

        if category is None:

                raise HTTPException(
                 status_code= 404,
                 detail="Category  not found"
           )

        
        result = await connection.execute(
                   
           text("""

                   UPDATE events 
                   SET
                       title = :title,
                       description = :description,
                       event_type = :event_type,
                       category_id = :category_id,
                       venue= :venue,
                       starts_at = :starts_at
                    WHERE id = :event_id

                    RETURNING 

                           id,
                           title,
                           description,
                           event_type,
                           category_id,
                           venue,
                           starts_at,
                           created_at



                   """),

    

        {
           
           "event_id" :event_id,
           "title":event.title,
           "description":event.description,
           "event_type":event.event_type.value,
           "category_id":event.category_id,
           "venue":event.venue,
           "starts_at":event.starts_at,


 
        })
        
        updated_event =result.fetchone()

        

        return{

             "id":updated_event.id,
             "title":updated_event.title,
             "description":updated_event.description,
             "event_type":updated_event.event_type,
             "category_id":updated_event.category_id,
             "venue":updated_event.venue,
             "starts_at":updated_event.starts_at,
             "created_at":updated_event.created_at,
        


        }

@app.delete("/events/{event_id}")

async def delete_event(event_id:int):

    async with engine.begin() as connection:

        # Check if event exsist

        result = await connection.execute(


            text("""
            


                   SELECT id FROM events WHERE id = :event_id

  
            
            
            
            
            """),


               {"event_id" : event_id}

        )

        event_to_be_deleted = result.fetchone() 


        if event_to_be_deleted is None:

                raise HTTPException(
                status_code= 404,
                detail="Event not found"
           )

           # Deleting the event
        
        result = await connection.execute(
               
               text("""
               

                     DELETE FROM events WHERE id=:event_id
               
               
               
               
               """),
                  
                {"event_id" : event_id}

                  
           

        )

        return {
            "message":"Event deleted Successfully"
        }


@app.post("/venues")

async def create_venue(venue:CreateVenue):

    async with engine.begin() as connection:


        result = await connection.execute(

                 text("""
                 
                         SELECT id FROM venues WHERE LOWER(name) = LOWER(:venue_name) AND  LOWER(location) = LOWER(:venue_location)
                 
                 """),
                    {"venue_name":venue.name,
                    "venue_location":venue.location}

        )


        new_data = result.fetchone()

        if new_data is not None:

                  raise HTTPException(
                status_code= 409,
                detail="Venue already exsists"
           )


        result = await connection.execute(

             text("""
             
                     INSERT INTO venues (name ,location) 

                     VALUES (:name,:location)
                     RETURNING id,name,location
             
             
             
             
             
             
             """),


                {   
                    "name":venue.name,
                
                    "location":venue.location                
                }

                 




        )

        new_venue = result.fetchone()

        return {

                  "id":new_venue.id,  
                 "name":new_venue.name,
                 "location":new_venue.location
        }


@app.get("/venues")

async def show_venues():

    async with engine.connect() as connection:

        result = await connection.execute(


            text("""
                  SELECT id,name,location FROM venues 
                    
            
            """)

               

               
        )

        venues = [
            {
               "id":row.id,
               "name":row.name,
               "location":row.location

            }

            for row in result
        ]

        return venues



@app.get("/venues/{venue_id}")

async def Show_event(venue_id:int):

    async with engine.connect() as connection:

        result = await connection.execute(

                text("""
                SELECT id,name,location FROM venues WHERE id =:venue_id
                """),{"venue_id":venue_id}




        )


        venue_data= result.fetchone()



        if venue_data is None:
                raise HTTPException(
                status_code= 404,
                detail="Venue not found"
           )


        return {

            "id":venue_data.id,
            "name":venue_data.name,
            "location":venue_data.location
        }





@app.put("/venues/{venue_id}")

async def Update_venue(venue_id:int ,venue:CreateVenue):

    async with engine.begin() as connection:

      

        result = await connection.execute(


              text (""" 
              
                       SELECT id from venues WHERE id = :venue_id
              
              
              
              
              
              """),{"venue_id":venue_id}





        )


        venue_data= result.fetchone()


        if venue_data is None:

              raise HTTPException(
                status_code= 404,
                detail="Venue not found"
           )


    try:

        
     async with engine.begin() as connection:

        result = await connection.execute(


             text(""" 
             
                    UPDATE venues 
                SET

                     
                     name=:name,
                     location=:location

                WHERE id=:venue_id


                RETURNING 

                         id,
                         name,
                         location

             
             
             
             
             """),

                {
                   "venue_id":venue_id,
                   "name":venue.name,
                   "location":venue.location

                }


           )


        updated_venue= result.fetchone()


    except IntegrityError:
     raise HTTPException(
        status_code=409,
        detail="A venue with this name and location already exists"
    )

    return {



                 "id":updated_venue.id,
                 "name":updated_venue.name,
                 "location":updated_venue.location
        }







@app.delete("/venues/{venue_id}")

async def delete_venue(venue_id:int):

    async with engine.begin() as connection:


               # Check if venue exsist
        

        result = await connection.execute(
            
               text(""" 
               
                       SELECT id FROM venues WHERE id = :venue_id
               
               
               
               """)  ,{"venue_id":venue_id}



        )



        venue= result.fetchone()


        if venue is None:
            raise HTTPException(
                status_code= 404,
                detail="Venue not found"
           )

            # Deleting the venue
        

        result = await connection.execute(

                text("DELETE FROM venues WHERE id= :venue_id "),

                {"venue_id":venue_id}


        )


        return {

            "message":"Venue deleted Successfully"
        }
        
        


        