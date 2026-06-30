from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Literal
from .database import vehicles_db, save_to_disk, verify_admin_token

# initiate the router module instead of a full app instance 
router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles Management"]
)

class vehicleCreate(BaseModel):
    # enforce standard plate formatting eg: kl-54-e-5454 using regex patterns
    registration_number: str = Field(..., pattern=r"^[A-Z]{2}-\d{2}-[A-Z]{1,2}-\d{4}$", description="License plate matching format like KL-07-CD-1234")
    model_name: str = Field(..., min_length=2, max_length=50)
    # enforce choices for the category 
    vehicle_name: Literal['car', 'bike', 'bus', 'truck', 'van']
    status: str = "AVAILABLE"
    total_trips: int = 0

@router.post("/create")
async def register_vehicle(vehicle: vehicleCreate, token: str = Depends(verify_admin_token)):
    key = vehicle.registration_number

    if key in vehicles_db:
        raise HTTPException(status_code=400, detail="Vehicle registration already exists")

    vehicles_db[key] = vehicle.model_dump()

    save_to_disk()
    return {
        "message": "vehicle registered successfully",
        "data": vehicles_db[key]
    }

@router.get('')
async def ger_all_vehicles(status: str = None, vehicle_name: str = None):
    if not status and not vehicle_name:
        return vehicles_db

    filtered_results = {}

    for reg_num, data in vehicles_db.items():
        # build logical matching flags
        match_status = (status is None or data.get('status', '').upper() == status.upper())
        match_type = (vehicle_name is None or data.get('vehicle_name', '').lower() == vehicle_name.lower())

        if match_status and match_type:
            filtered_results[reg_num] = data

    return filtered_results

@router.get('/vehicles/{registration_number}')
async def get_vehicle(registration_number: str):
    if registration_number not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle registration not found")
    
    return vehicles_db[registration_number]

@router.patch('/vehicles/{registration_number}/status')
async def update_status(registration_number: str, status: str, token: str = Depends(verify_admin_token)):
    if registration_number not in vehicles_db:
        raise HTTPException(status_code=404, detail="Vehicle registration not found")
    
    vehicle = vehicles_db[registration_number]
    vehicle['status'] = status

    save_to_disk()
    return {
        "message": "status updated successfully",
        "data": vehicle
    }

