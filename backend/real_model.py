import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

print("📂 Real dataset load ho raha hai...")
df = pd.read_csv('../data/DataSet.csv')
print(f"✅ {len(df)} rows, {len(df.columns)} columns loaded!")

# Last column target hai
target_col = df.columns[-1]
print(f"\n🎯 Target column: {target_col}")
print(f"Target values: {df[target_col].value_counts().to_dict()}")

# Numeric columns select karo
print("\n🔧 Features prepare ho rahi hain...")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if target_col in numeric_cols:
    numeric_cols.remove(target_col)

# Top 50 features use karo (fast training)
feature_cols = numeric_cols[:200]
print(f"✅ {len(feature_cols)} features selected")

X = df[feature_cols].fillna(0)
y = df[target_col]

# Target encode karo agar string hai
if y.dtype == 'object':
    le = LabelEncoder()
    y = le.fit_transform(y.astype(str))
    print(f"Classes: {le.classes_}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n🤖 Model train ho raha hai...")
print(f"Training samples: {len(X_train)}")
model = RandomForestClassifier(
    n_estimators=50,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("✅ Model ready!")

# Results
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\n📊 Accuracy: {acc*100:.1f}%")
print(classification_report(y_test, y_pred))

# Save
pickle.dump(model, open('../data/real_fraud_model.pkl', 'wb'))
print("✅ Real model saved!")

# Sample score
sample = X_test.iloc[0:1]
score = model.predict_proba(sample)[0]
print(f"\n🔍 Sample Fraud Score: {max(score)*100:.1f}%")