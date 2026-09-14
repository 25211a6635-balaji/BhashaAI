import joblib

from sklearn.metrics import confusion_matrix
from scipy.sparse import hstack


print("Loading BhashaAI v3...")


# ==========================================
# LOAD V3 MODEL
# ==========================================

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


print()
print(
    "Development sentences:",
    len(texts)
)


# ==========================================
# CREATE FEATURES
# ==========================================

print()
print("Creating v3 features...")


X = vectorizer.transform(
    texts
)


# ==========================================
# PREDICTIONS
# ==========================================

print("Running v3 predictions...")


predictions = model.predict(
    X
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

labels_order = [
    "AWA",
    "BHO",
    "BRA",
    "HIN",
    "MAG"
]


matrix = confusion_matrix(
    labels,
    predictions,
    labels=labels_order
)


print()
print("==========================================")
print("       BHASHAAI V3 ERROR ANALYSIS")
print("==========================================")


print()

print(
    "             Predicted"
)

print(
    "             AWA   BHO   BRA   HIN   MAG"
)


for i, label in enumerate(labels_order):

    print(
        f"Actual {label:<3}",
        matrix[i]
    )


# ==========================================
# COMMON MISTAKES
# ==========================================

print()
print("==========================================")
print("           COMMON MISTAKES")
print("==========================================")


errors = []


for i in range(
    len(labels_order)
):

    for j in range(
        len(labels_order)
    ):

        if i != j:

            errors.append(
                (
                    matrix[i][j],
                    labels_order[i],
                    labels_order[j]
                )
            )


errors.sort(
    reverse=True
)


for count, actual, predicted in errors[:10]:

    print(
        f"{actual} → {predicted}: {count}"
    )


print()
print("V3 error analysis completed! ✅")