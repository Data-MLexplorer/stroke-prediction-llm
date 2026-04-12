# Stroke Risk Prediction

An AI-powered stroke risk prediction web app built with **FastAPI** (backend) and **Streamlit** (frontend), using a trained machine learning model and an OpenAI-powered health assistant.

---

## Project Structure

```
stroke-risk/
│
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend
├── requirements.txt        # Python dependencies
│
├── model/
│   └── lr_pipeline.pkl     # Trained ML pipeline (scikit-learn)
│
└── README.md
```

---

## Features

- Patient data input form (gender, age, BMI, glucose, smoking status, etc.)
- Stroke risk probability score with a visual gauge
- Color-coded risk level — Low / Medium / High
- Contributing risk factors panel with severity bars
- AI Health Assistant powered by OpenAI GPT-4o
- FastAPI backend with input validation via Pydantic

---

## Setup

### 1. Clone the repo

```bash

https://github.com/Data-MLexplorer/stroke-prediction-llm.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your trained model

Place your trained scikit-learn pipeline at:

```
model/lr_pipeline.pkl
```

If you need to regenerate it, make sure it was saved with:

```python
import pickle
with open('model/lr_pipeline.pkl', 'wb') as f:
    pickle.dump(pipeline, f)
```

---

## Running the App

You need to run **both** the FastAPI backend and the Streamlit frontend.

### Start the FastAPI backend

```bash
uvicorn main:app --reload --port 8000
```

### Start the Streamlit frontend (in a new terminal)

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## API Endpoints

| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | `/health`  | Check if the backend is running    |
| POST   | `/predict` | Submit patient data, get risk score|

### Sample `/predict` request

```json
{
  "gender": "Female",
  "age": 65,
  "hypertension": 1,
  "heart_disease": 1,
  "ever_married": 1,
  "work_type": "Private",
  "Residence_type": "Urban",
  "avg_glucose_level": 220.0,
  "bmi": 34.5,
  "smoking_status": "formerly smoked"
}
```

### Sample response

```json
{
  "probability": 87.3,
  "label": "High Risk",
  "color": "#e74c3c"
}
```

---

## Input Field Reference

| Field | Accepted Values |
|---|---|
| `gender` | `Male`, `Female`, `Other` |
| `hypertension` | `0`, `1` |
| `heart_disease` | `0`, `1` |
| `ever_married` | `0`, `1` |
| `work_type` | `Private`, `Self-employed`, `Govt_job`, `children`, `Never_worked` |
| `Residence_type` | `Urban`, `Rural` |
| `smoking_status` | `never smoked`, `formerly smoked`, `smokes`, `Unknown` |
| `age` | 0 – 120 |
| `bmi` | 10 – 60 |
| `avg_glucose_level` | 50 – 300 |

---

## AI Health Assistant

The chat assistant is powered by **OpenAI GPT-4o** and runs client-side — your API key is never sent to the FastAPI backend.

To use it:
1. Enter your OpenAI API key in the sidebar (`sk-...`)
2. Run a prediction first
3. Ask anything about the patient's risk profile

---

## Model Details

- Algorithm: Logistic Regression (inside a scikit-learn `Pipeline`)
- Features: 16 encoded columns after one-hot encoding of categorical variables
- Preprocessing: Standard scaling for numeric features, manual one-hot encoding for categoricals
- Target: `stroke` (binary — 0 = no stroke, 1 = stroke)

The model was trained on multiple data versions (original, SMOTE-oversampled, undersampled) and evaluated on accuracy, sensitivity, specificity, F1, balanced accuracy, and ROC-AUC.

---

## Requirements

```
fastapi
uvicorn
streamlit
pydantic
pandas
numpy
scikit-learn
imbalanced-learn
requests
openai
```

---

## Notes

- The ML model output is a probability estimate only. It is **not a medical diagnosis**.
- Always consult a qualified clinician for any medical decisions.
- The risk factor severity bars are based on clinical heuristics, not model feature importances.



<img width="774" height="744" alt="Screenshot 2026-04-12 at 2 48 17 PM" src="https://github.com/user-attachments/assets/3941a434-60c1-4f3c-bf4d-a4eec7990932" />
