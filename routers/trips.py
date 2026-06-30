import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .database import vehicles_db, trips_db, save_to_disk

# initiate the router module instead of a full app instance 
router = APIRouter(
    prefix="/trips",
    tags=["Trip management"]
)


class TripsCreate(BaseModel):
    passenger_name: str
    pickup_location: str
    drop_location: str
    status: str = "Started"

# trips route
@router.post('')
async def create_trip(trip: TripsCreate):
    
    trip_id = None

    for reg_num, vehicle_data in vehicles_db.items():
        if vehicle_data['status'] == 'AVAILABLE':
            vehicle_data['status'] = 'ON_TRIP'
        
            trip_id = uuid.uuid4().hex
            trip_dict = trip.model_dump()
            trip_dict['registration_number'] = reg_num
            trips_db[trip_id] = trip_dict
            
            return {
                "message": "trip created successfully",
                "data": trips_db[trip_id]
            }

    save_to_disk()
    return {
        'message': 'No available vehicles at the moment'
    }

@router.get('')
async def ll_trips():
    return trips_db
    
# trip complete
@router.patch('/{trip_id}/complete')
async def complete_trip(trip_id: str):

    if trip_id not in trips_db:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    trip = trips_db[trip_id]

    if trip['status'] == "Completed":
        return {
            'message': 'trip already completed'
        }
    
    trip['status'] = "Completed"

    vehicle = vehicles_db[trip['registration_number']]
    vehicle['status'] = "AVAILABLE"

    current_trips = vehicle.get('total_trips', 0)
    vehicle['total_trips'] = current_trips + 1

    save_to_disk()
    return {
        "message": "trip completed successfully",
        "data": trip
    }