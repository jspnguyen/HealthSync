import fastapi
from pydantic import BaseModel
import json

app = fastapi.FastAPI()

class Patient(BaseModel):
    description: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/walkin/")
def walkin(patient: Patient):
    json = patient.model_dump()
    with open("json/patients.json", "w") as f:
        f.write(str(json).replace("'", "\""))
    return {"Status": "Success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)