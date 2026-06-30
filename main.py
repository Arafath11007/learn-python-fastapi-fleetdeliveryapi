from fastapi import FastAPI
from routers import vehicles, trips
from fastapi.middleware.cors import CORSMiddleware

# initiate the fast api app instance
app = FastAPI(title="Smart Fleet Management Engine")

# allow your react development server origin to pass through the security layer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, PATCH, OPTIONS, etc.
    allow_headers=["*"],  # Allows headers like X-Admin-Token
)

# est the POST endpoint to process the payload 
app.include_router(vehicles.router)
app.include_router(trips.router)