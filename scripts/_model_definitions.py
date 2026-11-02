# Model configurations recovered from the final MSc analysis notebook.
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
numerical_features = ["age_years", "BMI", "ap_hi", "ap_lo"]
categorical_features = ["gender", "cholesterol", "gluc", "smoke", "alco", "active"]
preprocessor = ColumnTransformer([("num", StandardScaler(), numerical_features), ("cat", "passthrough", categorical_features)])
models = {
    "Logistic Regression": Pipeline([
        ("preprocessor", preprocessor),
        ("model", LogisticRegression(max_iter=2000, random_state=42))
    ]),
    "Decision Tree": Pipeline([
        ("preprocessor", preprocessor),
        ("model", DecisionTreeClassifier(random_state=42))
    ]),
    "Random Forest (Tuned)": Pipeline([
        ("preprocessor", preprocessor),
        ("model", RandomForestClassifier(
            n_estimators=300,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=8,
            max_features="log2",
            random_state=42,
            n_jobs=-1
        ))
    ]),
    "AdaBoost": Pipeline([
        ("preprocessor", preprocessor),
        ("model", AdaBoostClassifier(random_state=42))
    ]),
    "Linear SVM": Pipeline([
        ("preprocessor", preprocessor),
        ("model", LinearSVC(random_state=42))
    ]),
    "KNN (Tuned)": Pipeline([
        ("preprocessor", preprocessor),
        ("model", KNeighborsClassifier(
            n_neighbors=41,
            weights="uniform",
            p=1,
            n_jobs=-1
        ))
    ]),
    "Gaussian Naive Bayes": Pipeline([
        ("preprocessor", preprocessor),
        ("model", GaussianNB())
    ])
}

