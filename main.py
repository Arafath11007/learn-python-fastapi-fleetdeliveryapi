from fastapi import FastAPI

from routers import vehicles, trips

# initiate the fast api app instance
app = FastAPI(title="Smart Fleet Management Engine")

# setup the in-memory database
vehicles_db = {}
trips_db = {}

# est the POST endpoint to process the payload 
app.include_router(vehicles.router)
app.include_router(trips.router)