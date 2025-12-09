import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

print("Carregando dataset modo apresentação...")
df = pd.read_csv("src/ia/tasks_dataset.csv")

le_category = LabelEncoder()
df["category_encoded"] = le_category.fit_transform(df["category"])

priority_map = {"Baixa": 0, "Média": 1, "Alta": 2}
df["priority_encoded"] = df["priority_label"].map(priority_map)

X = df[["days_until_due", "estimated_minutes", "difficulty", "category_encoded"]]
y = df["priority_encoded"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Treinando modelo...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n--- Resultado Final ---")
print(f"Acurácia: {accuracy:.2f}")
print(classification_report(y_test, y_pred, target_names=["Baixa", "Média", "Alta"]))

joblib.dump(model, "src/ia/kairos_model.pkl")
joblib.dump(le_category, "src/ia/category_encoder.pkl")
print("Modelo de apresentação salvo! 🧠")
