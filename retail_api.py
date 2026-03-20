"""FastAPI backend for the Retail Intelligence System.

This service trains all required ML models at startup using retail_data.py,
and exposes a /predict endpoint for the Next.js frontend.
"""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.tree import DecisionTreeClassifier

from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.models import Sequential

from retail_data import (
    FEATURES,
    X_test_c,
    X_test_r,
    X_test_s,
    X_train_c,
    X_train_r,
    X_train_s,
    scaler,
    y_test_c,
    y_test_r,
    y_train_c,
    y_train_r,
)

DAY_OPTIONS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
STORE_OPTIONS = ["Supermarket", "Hypermarket", "Convenience"]
CATEGORY_OPTIONS = ["Staples", "Snacks", "Beverages", "Personal", "Household", "Bakery", "Canned"]
CUSTOMER_OPTIONS = ["Member", "Normal"]
GENDER_OPTIONS = ["Male", "Female"]
PAYMENT_OPTIONS = ["Cash", "Credit Card", "E-Wallet", "GCash"]


class PredictionInput(BaseModel):
    quantity: float = Field(..., ge=0)
    unit_price: float = Field(..., ge=0)
    discount_pct: float = Field(..., ge=0)
    month: int = Field(..., ge=1, le=12)
    is_weekend: int = Field(..., ge=0, le=1)
    day_of_week: Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    store_type: Literal["Supermarket", "Hypermarket", "Convenience"]
    category: Literal["Staples", "Snacks", "Beverages", "Personal", "Household", "Bakery", "Canned"]
    customer_type: Literal["Member", "Normal"]
    gender: Literal["Male", "Female"]
    payment_method: Literal["Cash", "Credit Card", "E-Wallet", "GCash"]


class PredictionOutput(BaseModel):
    predictions: dict[str, str]


# Train all models at startup.
lr_model = LinearRegression()
lr_model.fit(X_train_r, y_train_r)

log_model = LogisticRegression(max_iter=10000, random_state=42)
log_model.fit(X_train_c, y_train_c)

dt_model = DecisionTreeClassifier(max_depth=4, random_state=42)
dt_model.fit(X_train_c, y_train_c)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_c, y_train_c)

nn_model = Sequential(
    [
        Input(shape=(len(FEATURES),)),
        Dense(64, activation="relu"),
        Dropout(0.2),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid"),
    ]
)
nn_model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
nn_model.fit(X_train_s, y_train_c, epochs=30, validation_split=0.1, verbose=0)

# Startup quality log for sanity checks.
lr_pred = lr_model.predict(X_test_r)
log_pred = log_model.predict(X_test_c)
dt_pred = dt_model.predict(X_test_c)
rf_pred = rf_model.predict(X_test_c)
_, nn_acc = nn_model.evaluate(X_test_s, y_test_c, verbose=0)
print("[retail_api] Linear Regression MSE:", round(mean_squared_error(y_test_r, lr_pred), 6))
print("[retail_api] Linear Regression R2:", round(r2_score(y_test_r, lr_pred), 6))
print("[retail_api] Logistic Accuracy:", round(accuracy_score(y_test_c, log_pred), 6))
print("[retail_api] Decision Tree Accuracy:", round(accuracy_score(y_test_c, dt_pred), 6))
print("[retail_api] Random Forest Accuracy:", round(accuracy_score(y_test_c, rf_pred), 6))
print("[retail_api] Neural Net Accuracy:", round(float(nn_acc), 6))

app = FastAPI(title="Retail Intelligence API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
def predict(payload: PredictionInput) -> PredictionOutput:
    try:
        day_enc = DAY_OPTIONS.index(payload.day_of_week)
        store_enc = STORE_OPTIONS.index(payload.store_type)
        category_enc = CATEGORY_OPTIONS.index(payload.category)
        customer_enc = CUSTOMER_OPTIONS.index(payload.customer_type)
        gender_enc = GENDER_OPTIONS.index(payload.gender)
        payment_enc = PAYMENT_OPTIONS.index(payload.payment_method)

        subtotal = payload.quantity * payload.unit_price * (1 - payload.discount_pct / 100)
        discount_amount = payload.quantity * payload.unit_price * payload.discount_pct / 100
        tax = subtotal * 0.12

        features = [[
            payload.quantity,
            payload.unit_price,
            payload.discount_pct,
            discount_amount,
            subtotal,
            tax,
            payload.month,
            payload.is_weekend,
            store_enc,
            category_enc,
            customer_enc,
            gender_enc,
            payment_enc,
            day_enc,
        ]]

        features_scaled = scaler.transform(features)

        lr_value = float(lr_model.predict(features)[0])
        log_value = int(log_model.predict(features)[0])
        dt_value = int(dt_model.predict(features)[0])
        rf_value = int(rf_model.predict(features)[0])
        nn_raw = float(nn_model.predict(features_scaled, verbose=0)[0][0])

        predictions = {
            "linear_regression": f"PHP {lr_value:,.2f}",
            "logistic_regression": "HIGH Sale" if log_value == 1 else "LOW Sale",
            "decision_tree": "HIGH Sale" if dt_value == 1 else "LOW Sale",
            "random_forest": "HIGH Sale" if rf_value == 1 else "LOW Sale",
            "neural_network": f"HIGH Sale ({nn_raw:.0%})" if nn_raw >= 0.5 else f"LOW Sale ({nn_raw:.0%})",
        }

        return PredictionOutput(predictions=predictions)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {exc}") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("retail_api:app", host="0.0.0.0", port=8000, reload=True)
