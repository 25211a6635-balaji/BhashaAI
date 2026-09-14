import joblib


# ==========================================
# LOAD V3 MODEL
# ==========================================

model = joblib.load(
    "dialect_model_v3.pkl"
)

vectorizer = joblib.load(
    "char_vectorizer_v3.pkl"
)


variety_names = {

    "HIN": "Hindi",

    "BRA": "Braj",

    "AWA": "Awadhi",

    "BHO": "Bhojpuri",

    "MAG": "Magahi"

}


print()
print("==========================================")
print("       BHASHAAI V3 CUSTOM TEST")
print("==========================================")

print()
print("Enter a sentence.")
print("Type 'exit' to stop.")
print()


while True:

    sentence = input(
        "Sentence: "
    ).strip()


    if sentence.lower() == "exit":

        break


    if not sentence:

        print(
            "Please enter a sentence."
        )

        continue


    # Create features

    X = vectorizer.transform(
        [sentence]
    )


    # Prediction

    prediction = model.predict(
        X
    )[0]


    # Probabilities

    probabilities = (
        model.predict_proba(X)[0]
    )


    best_index = probabilities.argmax()

    confidence = (
        probabilities[best_index] * 100
    )


    print()

    print(
        "Detected dialect:",
        variety_names[prediction]
    )

    print(
        f"Confidence: {confidence:.2f}%"
    )


    print()
    print("Probabilities:")


    for code, probability in zip(
        model.classes_,
        probabilities
    ):

        print(
            f"{variety_names[code]:10} "
            f"{probability * 100:.2f}%"
        )


    print()
    print("------------------------------------------")