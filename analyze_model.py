import joblib

from sklearn.metrics import confusion_matrix
from scipy.sparse import hstack


print("Loading BhashaAI model...")

model = joblib.load(
    "dialect_model.pkl"
)

char_vectorizer = joblib.load(
    "char_vectorizer.pkl"
)

word_vectorizer = joblib.load(
    "word_vectorizer.pkl"
)

print("Model loaded successfully! ✅")


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
print("Creating features...")


X_char = char_vectorizer.transform(
    texts
)

X_word = word_vectorizer.transform(
    texts
)

X = hstack([
    X_char,
    X_word
])


# ==========================================
# PREDICTIONS
# ==========================================

print("Running predictions...")


predictions = model.predict(X)


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
print("        BHASHAAI V3 ERROR ANALYSIS")
print("==========================================")


print()

print(
    "             Predicted"
)

print(
    "             AWA   BHO   BRA   HIN   MAG"
)

print(
    "Actual AWA ",
    matrix[0]
)

print(
    "Actual BHO ",
    matrix[1]
)

print(
    "Actual BRA ",
    matrix[2]
)

print(
    "Actual HIN ",
    matrix[3]
)

print(
    "Actual MAG ",
    matrix[4]
)


# ==========================================
# MOST COMMON ERRORS
# ==========================================

print()
print("==========================================")
print("           COMMON MISTAKES")
print("==========================================")


errors = []


for i in range(len(labels_order)):

    for j in range(len(labels_order)):

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
print("Analysis completed! ✅")