import httpx
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from twilio.rest import Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN = "your_auth_token_here"
TWILIO_PHONE_NUMBER = "+1855XXXXXXX"
USER_PHONE_NUMBER = "+1XXXXXXXXXX" 

active_database_medicines = ["Aspirin", "Ibuprofen"]

class MedicineCreate(BaseModel):
    name: str
    dosage: str
    time: str
    frequency: str

@app.post("/api/medicines")
async def add_and_check_medicine(med: MedicineCreate):
  
    fda_url = f"https://fda.gov:{med.name}&limit=1"
    
    warnings_found = ""
    async with httpx.AsyncClient() as client:
        try:
            fda_response = await client.get(fda_url)
            if fda_response.status_code == 200:
                fda_data = fda_response.json()
                results = fda_data.get("results", [{}])[0]
                
                warnings_list = results.get("warnings", [])
                if warnings_list:
                    warnings_found = " ".join(warnings_list)
        except Exception as e:
            print(f"openFDA connection offline: {e}")

   
    detected_conflicts = [existing_med for existing_med in active_database_medicines if existing_med.lower() in warnings_found.lower()]

    if detected_conflicts:
        conflict_msg = f"⚠️ Alert: {med.name} may interact with your active prescription: {', '.join(detected_conflicts)}."
         
        try:
            twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            twilio_client.messages.create(
                body=f"MedMinder Safety Flag: A conflict was caught during your entry log! {conflict_msg}",
                from_=TWILIO_PHONE_NUMBER,
                to=USER_PHONE_NUMBER
            )
        except Exception as sms_error:
            print(f"Twilio gateway error: {sms_error}")

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=conflict_msg
        )

    active_database_medicines.append(med.name)
    return {"success": True, "message": "Medication added successfully with zero flagged interactions."}
