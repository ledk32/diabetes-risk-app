from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_diabetes

app = FastAPI(title="Diabetes Prediction API")


class DiabetesInput(BaseModel):
    glucose: float
    blood_pressure: float
    skinfold: float
    insulin: float
    bmi: float
    diabetes_pedigree: float
    age: float


@app.post("/predict")
def predict(data: DiabetesInput):

    result = predict_diabetes(
        glucose=data.glucose,
        blood_pressure=data.blood_pressure,
        skinfold=data.skinfold,
        insulin=data.insulin,
        bmi=data.bmi,
        diabetes_pedigree=data.diabetes_pedigree,
        age=data.age
    )

    return {"prediction": result}