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