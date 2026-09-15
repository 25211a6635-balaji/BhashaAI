from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import joblib


# ============================================================
# BHASHAAI - LIGHTWEIGHT RENDER VERSION
# ============================================================

app = FastAPI(
    title="BhashaAI",
    description="Indian Dialect Identification",
    version="4.0"
)


# ============================================================
# FRONTEND
# ============================================================

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOAD DIALECT MODEL
# ============================================================

print()
print("==========================================")
print("       BHASHAAI RENDER VERSION")
print("==========================================")
print()

print("Loading dialect model...")

model = joblib.load(
    "dialect_model.pkl"
)

char_vectorizer = joblib.load(
    "char_vectorizer.pkl"
)

print("Dialect model loaded successfully! ✅")


# ============================================================
# DIALECT NAMES
# ============================================================

variety_names = {
    "HIN": "Hindi",
    "BRA": "Braj",
    "AWA": "Awadhi",
    "BHO": "Bhojpuri",
    "MAG": "Magahi"
}


# ============================================================
# INPUT MODEL
# ============================================================

class TextInput(BaseModel):
    text: str


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
def home():
    return FileResponse(
        "frontend/index.html"
    )


# ============================================================
# PREDICT DIALECT
# ============================================================

@app.post("/predict")
def predict(data: TextInput):

    sentence = data.text.strip()

    # --------------------------------------------------------
    # EMPTY INPUT
    # --------------------------------------------------------

    if not sentence:
        return {
            "error": "Please enter a sentence."
        }

    # --------------------------------------------------------
    # CREATE FEATURES
    # --------------------------------------------------------

    sentence_features = char_vectorizer.transform(
        [sentence]
    )

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    prediction = model.predict(
        sentence_features
    )[0]

    probabilities = model.predict_proba(
        sentence_features
    )[0]

    # --------------------------------------------------------
    # PROBABILITIES
    # --------------------------------------------------------

    probability_result = {}

    for code, probability in zip(
        model.classes_,
        probabilities
    ):

        probability_result[code] = round(
            probability * 100,
            2
        )

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    confidence = probability_result[
        prediction
    ]

    # --------------------------------------------------------
    # DISPLAY IN RENDER LOGS
    # --------------------------------------------------------

    print()
    print("==========================================")
    print("          BHASHAAI PREDICTION")
    print("==========================================")

    print(
        "Input:",
        sentence
    )

    print(
        "Detected dialect:",
        variety_names[prediction]
    )

    print(
        "Confidence:",
        confidence,
        "%"
    )

    # --------------------------------------------------------
    # LIGHTWEIGHT VERSION
    #
    # VAK translation is intentionally NOT loaded here.
    # The original local app.py still contains VAK.
    # --------------------------------------------------------

    standard_hindi = sentence

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "input": sentence,

        "dialect_code": prediction,

        "dialect": variety_names[
            prediction
        ],

        "confidence": confidence,

        "probabilities": probability_result,

        "standard_hindi": standard_hindi
    }


# ============================================================
# STARTUP MESSAGE
# ============================================================

print()
print("==========================================")
print("       BHASHAAI RENDER READY! 🚀")
print("==========================================")
print()