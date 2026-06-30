import json
import os

CACHE_FILE = 'fleet_cache.json'

# database.py
vehicles_db = {}
trips_db = {}

def save_to_disk():
    """ serialize and flushes the in memory state out to a physical JSON file """
    payload = {
        "vehicles": vehicles_db,
        "trips": trips_db
    }

    with open(CACHE_FILE, "w") as f:
        json.dump(payload, f, indent=4)

def load_from_disk():
    """ read the json file back in to memory when the python process starts up."""
    global vehicles_db, trips_db
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                raw_data = json.load(f)
                # clear and update the memory mirror safely
                vehicles_db.clear()
                vehicles_db.update(raw_data.get("vehicles", {}))
                

                trips_db.clear()
                trips_db.update(raw_data.get("trips", {}))
        except:
            print("⚠️ Cache file corrupted or unreadable. Initializing blank states.")

# trigger an immediate historical data load the moment this module is imported
load_from_disk()



from fastapi import Header, HTTPException

ADMIN_SECRET_TOKEN = 'kochi-fleet-admin-2026'

async def verify_admin_token(x_admin_token: str = Header(None)):
    """
        fastapi dependency that reads 'X-admin-token' from incoming requests headers.
        blocks the request if there token is invalid or missing
    """

    if x_admin_token != ADMIN_SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin token")
    
    return x_admin_token