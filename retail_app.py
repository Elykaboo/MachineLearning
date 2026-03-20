"""End-to-end Retail Intelligence System app.

This script trains 5 machine learning models and launches a Tkinter GUI
for real-time prediction using user-entered transaction details.
"""

# Import everything requested from the data module.
from retail_data import *
import retail_data as data

import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    classification_report,
)
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.ensemble import RandomForestClassifier

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


# -----------------------------
# Model 1: Linear Regression
# -----------------------------
lr_model = LinearRegression()
lr_model.fit(X_train_r, y_train_r)

lr_pred = lr_model.predict(X_test_r)
lr_mse = mean_squared_error(y_test_r, lr_pred)
lr_rmse = np.sqrt(lr_mse)
lr_r2 = r2_score(y_test_r, lr_pred)

print("\n=== Model 1: Linear Regression ===")
print(f"MSE: {lr_mse:.4f}")
print(f"RMSE: {lr_rmse:.4f}")
print(f"R^2: {lr_r2:.4f}")

# Persist trained model into retail_data module globals.
data.lr_model = lr_model


# -----------------------------
# Model 2: Logistic Regression
# -----------------------------
log_model = LogisticRegression(max_iter=10000, random_state=42)
log_model.fit(X_train_c, y_train_c)

log_pred = log_model.predict(X_test_c)
log_acc = accuracy_score(y_test_c, log_pred)

print("\n=== Model 2: Logistic Regression ===")
print(f"Accuracy: {log_acc:.4f}")
print(
    classification_report(
        y_test_c,
        log_pred,
        target_names=["Low Sale", "High Sale"],
        zero_division=0,
    )
)

# Persist trained model into retail_data module globals.
data.log_model = log_model


# -----------------------------
# Model 3: Decision Tree
# -----------------------------
dt_model = DecisionTreeClassifier(max_depth=4, random_state=42)
dt_model.fit(X_train_c, y_train_c)

dt_pred = dt_model.predict(X_test_c)
dt_acc = accuracy_score(y_test_c, dt_pred)

print("\n=== Model 3: Decision Tree ===")
print(f"Accuracy: {dt_acc:.4f}")
print("Rules (max depth shown = 2):")
print(export_text(dt_model, feature_names=FEATURES, max_depth=2))

# Persist trained model into retail_data module globals.
data.dt_model = dt_model


# -----------------------------
# Model 4: Random Forest
# -----------------------------
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_c, y_train_c)

rf_pred = rf_model.predict(X_test_c)
rf_acc = accuracy_score(y_test_c, rf_pred)

print("\n=== Model 4: Random Forest ===")
print(f"Accuracy: {rf_acc:.4f}")

importances = rf_model.feature_importances_
feature_importance_pairs = sorted(
    zip(FEATURES, importances), key=lambda x: x[1], reverse=True
)

print("Top 5 Feature Importances:")
for name, score in feature_importance_pairs[:5]:
    print(f"- {name}: {score:.4f}")

# Persist trained model into retail_data module globals.
data.rf_model = rf_model


# -----------------------------
# Model 5: Neural Network
# -----------------------------
nn_model = Sequential(
    [
        Dense(64, activation="relu", input_shape=(len(FEATURES),)),
        Dropout(0.2),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid"),
    ]
)

nn_model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

nn_model.fit(X_train_s, y_train_c, epochs=30, validation_split=0.1, verbose=0)

nn_loss, nn_acc = nn_model.evaluate(X_test_s, y_test_c, verbose=0)
print("\n=== Model 5: Neural Network ===")
print(f"Test Accuracy: {nn_acc:.4f}")

# Persist trained model into retail_data module globals.
data.nn_model = nn_model


# -----------------------------
# Tkinter GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Retail Intelligence System")
root.geometry("780x640")
root.configure(bg="#1E3A6E")

# Header labels.
header = tk.Label(
    root,
    text="Retail Intelligence System",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#1E3A6E",
)
header.pack(pady=(16, 6))

subtitle = tk.Label(
    root,
    text="Enter transaction details to get ML predictions",
    font=("Arial", 11),
    fg="#93C5FD",
    bg="#1E3A6E",
)
subtitle.pack(pady=(0, 14))

# Main input frame.
input_frame = tk.Frame(root, bg="white", padx=20, pady=10)
input_frame.pack(fill="x", padx=16, pady=8)

# Dropdown options in required order (used for index-based encoding).
day_options = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
store_options = ["Supermarket", "Hypermarket", "Convenience"]
category_options = [
    "Staples",
    "Snacks",
    "Beverages",
    "Personal",
    "Household",
    "Bakery",
    "Canned",
]
customer_options = ["Member", "Normal"]
gender_options = ["Male", "Female"]
payment_options = ["Cash", "Credit Card", "E-Wallet", "GCash"]

label_style = {"font": ("Arial", 10, "bold"), "fg": "#1E3A6E", "bg": "white"}

# Left column fields.
tk.Label(input_frame, text="Quantity:", **label_style).grid(
    row=0, column=0, sticky="w", padx=(0, 8), pady=6
)
ent_quantity = tk.Entry(input_frame)
ent_quantity.insert(0, "10")
ent_quantity.grid(row=0, column=1, sticky="w", pady=6)

tk.Label(input_frame, text="Unit Price (PHP):", **label_style).grid(
    row=1, column=0, sticky="w", padx=(0, 8), pady=6
)
ent_unit_price = tk.Entry(input_frame)
ent_unit_price.insert(0, "150")
ent_unit_price.grid(row=1, column=1, sticky="w", pady=6)

tk.Label(input_frame, text="Discount (%):", **label_style).grid(
    row=2, column=0, sticky="w", padx=(0, 8), pady=6
)
ent_discount = tk.Entry(input_frame)
ent_discount.insert(0, "10")
ent_discount.grid(row=2, column=1, sticky="w", pady=6)

tk.Label(input_frame, text="Month (1-12):", **label_style).grid(
    row=3, column=0, sticky="w", padx=(0, 8), pady=6
)
ent_month = tk.Entry(input_frame)
ent_month.insert(0, "6")
ent_month.grid(row=3, column=1, sticky="w", pady=6)

tk.Label(input_frame, text="Day of Week:", **label_style).grid(
    row=4, column=0, sticky="w", padx=(0, 8), pady=6
)
cb_day = ttk.Combobox(input_frame, values=day_options, state="readonly", width=18)
cb_day.set("Monday")
cb_day.grid(row=4, column=1, sticky="w", pady=6)

var_weekend = tk.IntVar(value=0)
chk_weekend = tk.Checkbutton(
    input_frame,
    text="Weekend?",
    variable=var_weekend,
    bg="white",
    font=("Arial", 10, "bold"),
    fg="#1E3A6E",
    activebackground="white",
)
chk_weekend.grid(row=5, column=0, columnspan=2, sticky="w", pady=6)

# Right column fields.
tk.Label(input_frame, text="Store Type:", **label_style).grid(
    row=0, column=2, sticky="w", padx=(24, 8), pady=6
)
cb_store = ttk.Combobox(input_frame, values=store_options, state="readonly", width=18)
cb_store.set("Supermarket")
cb_store.grid(row=0, column=3, sticky="w", pady=6)

tk.Label(input_frame, text="Product Category:", **label_style).grid(
    row=1, column=2, sticky="w", padx=(24, 8), pady=6
)
cb_category = ttk.Combobox(
    input_frame, values=category_options, state="readonly", width=18
)
cb_category.set("Staples")
cb_category.grid(row=1, column=3, sticky="w", pady=6)

tk.Label(input_frame, text="Customer Type:", **label_style).grid(
    row=2, column=2, sticky="w", padx=(24, 8), pady=6
)
cb_customer = ttk.Combobox(
    input_frame, values=customer_options, state="readonly", width=18
)
cb_customer.set("Member")
cb_customer.grid(row=2, column=3, sticky="w", pady=6)

tk.Label(input_frame, text="Gender:", **label_style).grid(
    row=3, column=2, sticky="w", padx=(24, 8), pady=6
)
cb_gender = ttk.Combobox(input_frame, values=gender_options, state="readonly", width=18)
cb_gender.set("Male")
cb_gender.grid(row=3, column=3, sticky="w", pady=6)

tk.Label(input_frame, text="Payment:", **label_style).grid(
    row=4, column=2, sticky="w", padx=(24, 8), pady=6
)
cb_payment = ttk.Combobox(
    input_frame, values=payment_options, state="readonly", width=18
)
cb_payment.set("Cash")
cb_payment.grid(row=4, column=3, sticky="w", pady=6)


# -----------------------------
# Prediction function for all models
# -----------------------------
def predict_all():
    """Read user input, build features, run all 5 model predictions, and display results."""
    try:
        # 1) Read numeric inputs.
        qty = float(ent_quantity.get())
        unit_price = float(ent_unit_price.get())
        discount = float(ent_discount.get())
        month = int(ent_month.get())
        is_weekend = int(var_weekend.get())

        # 2) Encode categorical selections by index from fixed option lists.
        day_enc = day_options.index(cb_day.get())
        store_enc = store_options.index(cb_store.get())
        cat_enc = category_options.index(cb_category.get())
        cust_enc = customer_options.index(cb_customer.get())
        gender_enc = gender_options.index(cb_gender.get())
        pay_enc = payment_options.index(cb_payment.get())

        # 3) Derived business calculations.
        subtotal = qty * unit_price * (1 - discount / 100)
        discount_amount = qty * unit_price * discount / 100
        tax = subtotal * 0.12

        # 4) Build model feature vector in the exact shared FEATURES order.
        features = [
            [
                qty,
                unit_price,
                discount,
                discount_amount,
                subtotal,
                tax,
                month,
                is_weekend,
                store_enc,
                cat_enc,
                cust_enc,
                gender_enc,
                pay_enc,
                day_enc,
            ]
        ]

        # 5) Scale features for neural network only.
        features_scaled = scaler.transform(features)

        # 6) Get predictions from each model.
        lr_result = f"PHP {lr_model.predict(features)[0]:,.2f}"

        log_pred = log_model.predict(features)[0]
        log_result = "HIGH Sale" if log_pred == 1 else "LOW Sale"

        dt_pred = dt_model.predict(features)[0]
        dt_result = "HIGH Sale" if dt_pred == 1 else "LOW Sale"

        rf_pred = rf_model.predict(features)[0]
        rf_result = "HIGH Sale" if rf_pred == 1 else "LOW Sale"

        nn_raw = nn_model.predict(features_scaled, verbose=0)[0][0]
        nn_result = (
            f"HIGH Sale ({nn_raw:.0%})" if nn_raw >= 0.5 else f"LOW Sale ({nn_raw:.0%})"
        )

        # 7) Update result labels.
        lbl_lr.config(text=lr_result)
        lbl_log.config(text=log_result)
        lbl_dt.config(text=dt_result)
        lbl_rf.config(text=rf_result)
        lbl_nn.config(text=nn_result)

    except Exception as exc:
        # 8) Show friendly GUI error message if anything fails.
        messagebox.showerror("Prediction Error", f"Could not generate predictions:\n{exc}")


# Predict button.
btn_predict = tk.Button(
    root,
    text="Get Predictions from All 5 Models",
    command=predict_all,
    bg="#2563EB",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=8,
    relief="flat",
    cursor="hand2",
)
btn_predict.pack(pady=14)

# Results frame.
results_frame = tk.Frame(root, bg="white", padx=20, pady=6)
results_frame.pack(fill="x", padx=16, pady=8)

tk.Label(
    results_frame,
    text="Model Predictions",
    font=("Arial", 13, "bold"),
    fg="#1E3A6E",
    bg="white",
).grid(row=0, column=0, columnspan=2, sticky="w", pady=(2, 10))

model_label_style = {"font": ("Arial", 10, "bold"), "fg": "#374151", "bg": "white"}
result_label_style = {
    "font": ("Arial", 11),
    "fg": "#2563EB",
    "bg": "white",
    "width": 28,
    "anchor": "w",
}

tk.Label(results_frame, text="Linear Regression:", **model_label_style).grid(
    row=1, column=0, sticky="w", pady=4
)
lbl_lr = tk.Label(results_frame, text="---", **result_label_style)
lbl_lr.grid(row=1, column=1, sticky="w", pady=4)

tk.Label(results_frame, text="Logistic Regression:", **model_label_style).grid(
    row=2, column=0, sticky="w", pady=4
)
lbl_log = tk.Label(results_frame, text="---", **result_label_style)
lbl_log.grid(row=2, column=1, sticky="w", pady=4)

tk.Label(results_frame, text="Decision Tree:", **model_label_style).grid(
    row=3, column=0, sticky="w", pady=4
)
lbl_dt = tk.Label(results_frame, text="---", **result_label_style)
lbl_dt.grid(row=3, column=1, sticky="w", pady=4)

tk.Label(results_frame, text="Random Forest:", **model_label_style).grid(
    row=4, column=0, sticky="w", pady=4
)
lbl_rf = tk.Label(results_frame, text="---", **result_label_style)
lbl_rf.grid(row=4, column=1, sticky="w", pady=4)

tk.Label(results_frame, text="Neural Network:", **model_label_style).grid(
    row=5, column=0, sticky="w", pady=4
)
lbl_nn = tk.Label(results_frame, text="---", **result_label_style)
lbl_nn.grid(row=5, column=1, sticky="w", pady=4)

# Start the GUI event loop.
root.mainloop()
