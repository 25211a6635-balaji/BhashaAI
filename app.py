from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import joblib
import ctranslate2

from huggingface_hub import snapshot_download

from transformers import NllbTokenizer


# ============================================================
# BHASHAAI APPLICATION
# ============================================================

app = FastAPI(
    title="BhashaAI",
    description="Indian Dialect Identification and Standard Hindi Conversion",
    version="3.0"
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
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# LOAD DIALECT MODEL
# ============================================================

print()
print("==========================================")
print("          BHASHAAI STARTING")
print("==========================================")

print()
print("Loading BhashaAI dialect model...")

model = joblib.load(
    "dialect_model.pkl"
)

char_vectorizer = joblib.load(
    "char_vectorizer.pkl"
)

print("Dialect model loaded successfully! ✅")


# ============================================================
# VAK TRANSLATION MODEL
# ============================================================

VAK_MODEL_ID = "shunyalabs/vak-translate-1.3b-ct2"

VAK_MODEL_PATH = snapshot_download(
    repo_id=VAK_MODEL_ID
)


print()
print("Loading VAK translation tokenizer...")

tokenizer = NllbTokenizer.from_pretrained(
    VAK_MODEL_PATH
)

print("VAK tokenizer loaded successfully! ✅")


print()
print("Loading VAK translation model...")
print("This may take some time...")

translator = ctranslate2.Translator(
    VAK_MODEL_PATH,
    device="cpu"
)

print("VAK translation model loaded successfully! ✅")


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
# VAK LANGUAGE CODES
# ============================================================

vak_language_codes = {

    "HIN": "hin_Deva",

    "BRA": "brj_Deva",

    "AWA": "awa_Deva",

    "BHO": "bho_Deva",

    "MAG": "mag_Deva"

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
# TRANSLATE TO STANDARD HINDI
# ============================================================

def translate_to_standard_hindi(
    sentence,
    dialect_code
):

    source_language = vak_language_codes.get(
        dialect_code,
        "hin_Deva"
    )

    target_language = "hin_Deva"


    print()
    print(
        "VAK source language:",
        source_language
    )

    print(
        "VAK target language:",
        target_language
    )


    tokenizer.src_lang = source_language


    inputs = tokenizer(
        sentence
    )


    source_tokens = tokenizer.convert_ids_to_tokens(
        inputs["input_ids"]
    )


    results = translator.translate_batch(

        [source_tokens],

        target_prefix=[
            [target_language]
        ],

        beam_size=4,

        max_decoding_length=256
    )


    output_tokens = results[0].hypotheses[0]


    output_ids = tokenizer.convert_tokens_to_ids(
        output_tokens
    )


    translation = tokenizer.decode(
        output_ids,
        skip_special_tokens=True
    )


    return translation


# ============================================================
# PREDICT DIALECT
# ============================================================

@app.post("/predict")
def predict(data: TextInput):

    sentence = data.text.strip()


    if not sentence:

        return {
            "error": "Please enter a sentence."
        }


    # --------------------------------------------------------
    # V3 CHARACTER TF-IDF
    # --------------------------------------------------------

    sentence_features = char_vectorizer.transform(
        [sentence]
    )


    # --------------------------------------------------------
    # DIALECT PREDICTION
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


    confidence = probability_result[
        prediction
    ]


    print()
    print("==========================================")
    print("       BHASHAAI TRANSLATION")
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
    # TRANSLATION
    # --------------------------------------------------------

    try:

        standard_hindi = translate_to_standard_hindi(
            sentence,
            prediction
        )


        print(
            "Translation completed:",
            standard_hindi
        )


    except Exception as error:

        print(
            "Translation error:",
            error
        )


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
print("        BHASHAAI READY! 🚀")
print("==========================================")
print()