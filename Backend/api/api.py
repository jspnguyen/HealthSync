from fastapi import WebSocket
import fastapi
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append("..")
import main
import asyncio
import json
import time



app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Patient(BaseModel):
    description: str

class Counts(BaseModel):
    doctor_count: int
    nurse_count: int
    equipment_count: int
    patients_waiting_count: int
    patients_emergency_count: int
    bed_count: int


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/walkin/")
def walkin(patient: Patient):
    json = patient.model_dump()
    with open("json/patients.json", "w") as f:
        f.write(str(json).replace("'", "\""))
    return {"Status": "Success"}

@app.post("/counts/")
def walkin(counts: Counts):
    json = counts.model_dump()
    with open("json/counts.json", "w") as f:
        f.write(str(json).replace("'", "\""))
    return {"Status": "Success"}

@app.get("/graph")
def get_graph():
    with open("./json/graph.json", 'r') as f:
        graph = json.load(f)
    return graph

@app.get("/count/doctors")
def get_doctor_count():
    load = "Low"
    if main.doctor_id_counter < 10:
        load = "Low"
    elif main.doctor_id_counter >= 10:
        load = "Normal"

    return {"count": main.doctor_id_counter, "load": load}

@app.get("/count/nurses"):
def get_nurse_count():
    return {"count": main.get_nurse_count(), "load": }

@app.get("/count/equipment"):
def get_equipment_count():
    return {"count": main.get_equipment_count(), "load": }

@app.get("/count/patientswaiting"):
def get_patients_waiting_count():
    return {"count": main.get_patients_waiting_count(), "load": }

@app.get("/count/patientemergency"):
def get_patients_emergency_count():
    return {"count": main.get_patients_emergency_count(), "load": }




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)