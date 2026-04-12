from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from pydantic import BaseModel, field_validator
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import pickle
import json
import pandas as pd
import numpy as np

app = FastAPI(title="Stroke Prediction API")

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

# ── Load pipeline + feature columns ──────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / 'model/lr_pipeline.pkl', 'rb') as f:
    final_pipeline = pickle.load(f)

with open(BASE_DIR / 'model/feature_cols.json', 'r') as f:
    feature_cols = json.load(f)

# ── Valid categories ──────────────────────────────────────────────────────────
VALID_GENDER          = {'Male', 'Female', 'Other'}
VALID_WORK_TYPE       = {'Private', 'Self-employed', 'Govt_job', 'children', 'Never_worked'}
VALID_RESIDENCE       = {'Urban', 'Rural'}
VALID_SMOKING         = {'formerly smoked', 'never smoked', 'smokes', 'Unknown'}

# ── Input schema ──────────────────────────────────────────────────────────────
class PatientData(BaseModel):
    gender            : str
    age               : float
    hypertension      : int
    heart_disease     : int
    ever_married      : int
    work_type         : str
    Residence_type    : str
    avg_glucose_level : float
    bmi               : float
    smoking_status    : str

    # ── Validators ────────────────────────────────────────────────────────────
    @field_validator('gender')
    def validate_gender(cls, v):
        if v not in VALID_GENDER:
            raise ValueError(f"gender must be one of {VALID_GENDER}")
        return v

    @field_validator('work_type')
    def validate_work_type(cls, v):
        if v not in VALID_WORK_TYPE:
            raise ValueError(f"work_type must be one of {VALID_WORK_TYPE}")
        return v

    @field_validator('Residence_type')
    def validate_residence(cls, v):
        if v not in VALID_RESIDENCE:
            raise ValueError(f"Residence_type must be one of {VALID_RESIDENCE}")
        return v

    @field_validator('smoking_status')
    def validate_smoking(cls, v):
        if v not in VALID_SMOKING:
            raise ValueError(f"smoking_status must be one of {VALID_SMOKING}")
        return v

    @field_validator('age')
    def validate_age(cls, v):
        if not (0 <= v <= 120):
            raise ValueError("age must be between 0 and 120")
        return v

    @field_validator('bmi')
    def validate_bmi(cls, v):
        if not (10 <= v <= 60):
            raise ValueError("bmi must be between 10 and 60")
        return v

    @field_validator('avg_glucose_level')
    def validate_glucose(cls, v):
        if not (50 <= v <= 300):
            raise ValueError("avg_glucose_level must be between 50 and 300")
        return v

    @field_validator('hypertension', 'heart_disease', 'ever_married')
    def validate_binary(cls, v):
        if v not in (0, 1):
            raise ValueError("Must be 0 or 1")
        return v

# ── Feature builder ───────────────────────────────────────────────────────────
def build_features(data: PatientData) -> pd.DataFrame:
    raw = {
        'age'                            : data.age,
        'hypertension'                   : data.hypertension,
        'heart_disease'                  : data.heart_disease,
        'ever_married'                   : data.ever_married,
        'avg_glucose_level'              : data.avg_glucose_level,
        'bmi'                            : data.bmi,
        'gender_Male'                    : int(data.gender == 'Male'),
        'gender_Other'                   : int(data.gender == 'Other'),
        'work_type_Never_worked'         : int(data.work_type == 'Never_worked'),
        'work_type_Private'              : int(data.work_type == 'Private'),
        'work_type_Self-employed'        : int(data.work_type == 'Self-employed'),
        'work_type_children'             : int(data.work_type == 'children'),
        'Residence_type_Urban'           : int(data.Residence_type == 'Urban'),
        'smoking_status_formerly smoked' : int(data.smoking_status == 'formerly smoked'),
        'smoking_status_never smoked'    : int(data.smoking_status == 'never smoked'),
        'smoking_status_smokes'          : int(data.smoking_status == 'smokes'),
    }

    df = pd.DataFrame([{col: raw.get(col, 0) for col in feature_cols}])
    print(f"Features sent: {df.shape[1]} — {list(df.columns)}")
    return df

# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": final_pipeline is not None}

# ── Predict endpoint ──────────────────────────────────────────────────────────
@app.post("/predict")
async def predict(data: PatientData):
    try:
        df = build_features(data)

        probability = round(float(final_pipeline.predict_proba(df)[0][1]) * 100, 1)

        if probability >= 50:   label, color = "High Risk",   "#e74c3c"
        elif probability >= 30: label, color = "Medium Risk", "#f39c12"
        else:                   label, color = "Low Risk",    "#2ecc71"

        return {"probability": probability, "label": label, "color": color}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Prediction failed", "detail": str(e)}
        )