from fastapi import FastAPI

from api.daos.db_connector import neo4j_driver
from api.routers import persons, skills, relationships

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    neo4j_driver.open_connection()


@app.on_event("shutdown")
def shutdown_event():
    neo4j_driver.close_connection()


app.include_router(
    router=persons.router,
    prefix="/persons",
    tags=["persons"]
)

app.include_router(
    router=skills.router,
    prefix="/skills",
    tags=["skills"]
)

app.include_router(
    router=relationships.router,
    prefix="/relationships",
    tags=["relationships"]
)