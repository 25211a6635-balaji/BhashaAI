import joblib


print("Loading BhashaAI v3...")

model = joblib.load(
    "dialect_model_v3.pkl"
)

vectorizer = joblib.load(
    "char_vectorizer_v3.pkl"
)

print("V3 model loaded successfully! ✅")


# ==========================================
# LOAD DEVELOPMENT DATA
# ==========================================

texts = []
labels = []


with open(
    "dataset/dev.txt",
    "r",
    encoding="utf-8"
) as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        parts = line.rsplit(
            maxsplit=1
        )

        if len(parts) != 2:
            continue

        texts.append(parts[0])
        labels.append(parts[1])


# ==========================================
# CREATE FEATURES
# ==========================================

print()
print("Creating features...")

X = vectorizer.transform(
    texts
)


# ==========================================
# PREDICT
# ==========================================

print("Finding incorrect predictions...")

predictions = model.predict(X)


# ==========================================
# SHOW IMPORTANT ERRORS
# ==========================================

important_pairs = [
    ("MAG", "BHO"),
    ("BHO", "HIN"),
    ("MAG", "HIN")
]


print()
print("==========================================")
print("        BHASHAAI V3 SAMPLE ERRORS")
print("==========================================")


for actual, predicted in important_pairs:

    print()
    print("------------------------------------------")

    print(
        f"ACTUAL: {actual}  →  PREDICTED: {predicted}"
    )

    print("------------------------------------------")

    count = 0


    for i in range(
        len(texts)
    ):

        if (
            labels[i] == actual
            and
            predictions[i] == predicted
        ):

            print(
                f"{count + 1}. {texts[i]}"
            )

            count += 1


            if count == 10:
                break


print()
print("==========================================")
print("        ERROR ANALYSIS COMPLETE")
print("==========================================")