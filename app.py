from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
import uvicorn

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    city: Annotated[str, Field(...)]
    age: Annotated[int, Field(..., gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(...)]
    height: Annotated[float, Field(..., gt=0)]
    weight: Annotated[float, Field(..., gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        return "Obese"

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0, lt=120)
    gender: Optional[Literal['male', 'female', 'others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

def load_data():
    try:
        with open("patients.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=2)

@app.get("/")
def root():
    return {"message": "Patient Management System API"}

@app.get("/view")
def view():
    return load_data()

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """
    Update an existing patient's information.
    """
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    updated_fields = patient_update.model_dump(exclude_unset=True)
    data[patient_id].update(updated_fields)

    try:
        # Validate the updated patient data
        validated = Patient(id=patient_id, **data[patient_id])
        data[patient_id] = validated.model_dump(exclude=["id"])
        save_data(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Validation failed: {e}")

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return {"message": "Patient deleted successfully"}

@app.get("/sort")
def sort_patients(sort_by: str, order: str = "asc"):
    if sort_by not in ["height", "weight", "bmi"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    reverse = order == "desc"
    data = load_data()
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse
    )
    return sorted_data

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
