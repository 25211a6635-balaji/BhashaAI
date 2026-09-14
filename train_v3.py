from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib


# ==========================================
# LOAD TRAINING DATA
# ==========================================

train_texts = []
train_labels = []


with open(
    "dataset/train.txt",
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

        train_texts.append(parts[0])
        train_labels.append(parts[1])


print("Training sentences:", len(train_texts))


# ==========================================
# LOAD DEVELOPMENT DATA
# ==========================================

test_texts = []
test_labels = []


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

        test_texts.append(parts[0])
        test_labels.append(parts[1])


print(
    "Development sentences:",
    len(test_texts)
)


# ==========================================
# CHARACTER TF-IDF
# ==========================================

print()
print("Creating improved character features...")


vectorizer = TfidfVectorizer(

    analyzer="char",

    ngram_range=(2, 6),

    sublinear_tf=True,

    min_df=2,

    max_features=250000

)


X_train = vectorizer.fit_transform(
    train_texts
)

X_test = vectorizer.transform(
    test_texts
)


print(
    "Feature matrix:",
    X_train.shape
)


# ==========================================
# TRAIN MODEL
# ==========================================

print()
print("Training BhashaAI v3...")


model = LogisticRegression(

    max_iter=1000,

    C=2.0
)


model.fit(
    X_train,
    train_labels
)


print(
    "BhashaAI v3 training completed! 🤖"
)


# ==========================================
# TEST MODEL
# ==========================================

print()
print("Testing BhashaAI v3...")


predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    test_labels,
    predictions
)


# ==========================================
# RESULTS
# ==========================================

print()
print("==========================================")
print("       BHASHAAI V3 MODEL RESULTS")
print("==========================================")


print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


print()
print(
    "Previous best baseline: 94.66%"
)


improvement = (
    accuracy * 100
) - 94.66


print(
    f"Improvement: {improvement:+.2f} percentage points"
)


print()
print("Classification Report:")
print()


print(
    classification_report(
        test_labels,
        predictions,

        labels=[
            "AWA",
            "BHO",
            "BRA",
            "HIN",
            "MAG"
        ],

        target_names=[
            "Awadhi",
            "Bhojpuri",
            "Braj",
            "Hindi",
            "Magahi"
        ]
    )
)


# ==========================================
# SAVE V3 SEPARATELY
# ==========================================

print()
print("Saving BhashaAI v3...")


joblib.dump(
    model,
    "dialect_model_v3.pkl"
)


joblib.dump(
    vectorizer,
    "char_vectorizer_v3.pkl"
)


print(
    "V3 model saved successfully! ✅"
)


print()
print("==========================================")
print("              V3 COMPLETE")
print("==========================================")