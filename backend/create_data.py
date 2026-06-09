import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 500

accounts = [f"ACC{str(i).zfill(4)}" for i in range(1, 101)]

data = {
    "transaction_id": [f"TXN{str(i).zfill(5)}" for i in range(1, n+1)],
    "from_account": np.random.choice(accounts, n),
    "to_account": np.random.choice(accounts, n),
    "amount": np.random.choice([
        np.random.randint(1000, 10000),
        np.random.choice([10000, 20000, 25000, 50000])
    ], n),
    "timestamp": pd.date_range("2024-01-01", periods=n, freq="30min"),
    "channel": np.random.choice(["UPI", "NEFT", "IMPS", "RTGS"], n),
    "is_fraud": np.random.choice([0, 1], n, p=[0.85, 0.15])
}

df = pd.DataFrame(data)

os.makedirs("../data", exist_ok=True)
df.to_csv("../data/DataSet.csv", index=False)

print("✅ DataSet.csv ready!")
print(f"Total rows: {len(df)}")
print(f"Fraud cases: {df['is_fraud'].sum()}")
print(df.head()) 
