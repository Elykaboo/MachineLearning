"""Data preparation module for the Retail Intelligence System.

This module loads the retail sales dataset, creates engineered targets/features,
and exposes train/test splits plus shared objects for downstream model training.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load the dataset from the same directory as this script.
df = pd.read_csv("retail_sales.csv")

# Create binary target for classification tasks.
mean_total_sales = df["total_sales"].mean()
df["high_sale"] = (df["total_sales"] >= mean_total_sales).astype(int)

# Encode categorical fields and store encoded values with "_enc" suffix.
encode_columns = [
    "store_type",
    "category",
    "customer_type",
    "gender",
    "payment_method",
    "day_of_week",
]

label_encoders = {}
for col in encode_columns:
    encoder = LabelEncoder()
    df[f"{col}_enc"] = encoder.fit_transform(df[col].astype(str))
    label_encoders[col] = encoder

# Feature list used across all models.
FEATURES = [
    "quantity",
    "unit_price",
    "discount_pct",
    "discount_amount",
    "subtotal",
    "tax_amount",
    "month",
    "is_weekend",
    "store_type_enc",
    "category_enc",
    "customer_type_enc",
    "gender_enc",
    "payment_method_enc",
    "day_of_week_enc",
]

# Prepare regression inputs/targets.
X_reg = df[FEATURES]
y_reg = df["total_sales"]

# Prepare classification inputs/targets.
X_cls = df[FEATURES]
y_cls = df["high_sale"]

# Split regression dataset.
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

# Split classification dataset.
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_cls, y_cls, test_size=0.2, random_state=42
)

# Scale classification features ONLY for neural network usage.
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train_c)
X_test_s = scaler.transform(X_test_c)

# Global model placeholders to be filled by retail_app.py after training.
lr_model = None
log_model = None
dt_model = None
rf_model = None
nn_model = None


if __name__ == "__main__":
    # Print requested exploratory summaries only when run directly.
    print("Dataset shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nDescribe:")
    print(df.describe(include="all"))
    print("\nMissing values:")
    print(df.isnull().sum())
