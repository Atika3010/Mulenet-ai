import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# 1. Data load karo
print("📂 Data load ho raha hai...")
df = pd.read_csv('../data/DataSet.csv')
print(f"✅ {len(df)} rows loaded!")

# 2. Features banao
print("\n🔧 Features bana rahe hain...")
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
df['is_round_amount'] = (df['amount'] % 5000 == 0).astype(int)
df['is_night'] = ((df['hour'] >= 22) | (df['hour'] <= 6)).astype(int)

# Account wise stats
from_stats = df.groupby('from_account').agg(
    txn_count=('amount', 'count'),
    avg_amount=('amount', 'mean'),
    total_amount=('amount', 'sum')
).reset_index()
from_stats.columns = ['from_account', 'txn_count', 'avg_amount', 'total_amount']

df = df.merge(from_stats, on='from_account', how='left')

# 3. Model ke liye data prepare karo
features = ['amount', 'hour', 'is_round_amount', 'is_night',
            'txn_count', 'avg_amount', 'total_amount']

X = df[features]
y = df['is_fraud']

# 4. Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Model train karo
print("\n🤖 Model train ho raha hai...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("✅ Model ready!")

# 6. Results dekho
print("\n📊 Model Performance:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 7. Model save karo
pickle.dump(model, open('../data/fraud_model.pkl', 'wb'))
print("✅ Model saved!")

# 8. Sample prediction
print("\n🔍 Sample Fraud Score:")
sample = X_test.iloc[0:1]
score = model.predict_proba(sample)[0][1]
print(f"Fraud Probability: {score*100:.1f}%")