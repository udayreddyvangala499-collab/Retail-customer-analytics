import pandas as pd
import numpy as np

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("superstore.xlsx.csv", encoding='latin1')   # change if filename differs

# =========================
# COPY DATA
# =========================
df_clean = df.copy()

# =========================
# CLEAN COLUMN NAMES
# =========================
df_clean.columns = df_clean.columns.str.strip()

# =========================
# REMOVE DUPLICATES
# =========================
df_clean = df_clean.drop_duplicates()

# =========================
# CLEAN TEXT COLUMNS
# =========================
for col in df_clean.select_dtypes(include="object").columns:
    df_clean[col] = df_clean[col].astype(str).str.strip()
    df_clean[col] = df_clean[col].replace("nan", np.nan)

# =========================
# FIX DATE COLUMNS
# =========================
df_clean["Order Date"] = pd.to_datetime(
    df_clean["Order Date"], format="%m/%d/%Y", errors="coerce"
)

df_clean["Ship Date"] = pd.to_datetime(
    df_clean["Ship Date"], format="%m/%d/%Y", errors="coerce"
)

# =========================
# CONVERT NUMERIC COLUMNS
# =========================
for col in ["Sales", "Quantity", "Discount", "Profit", "Postal Code"]:
    df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# =========================
# FILL MISSING VALUES
# =========================
df_clean["Order Date"] = df_clean["Order Date"].fillna(df_clean["Order Date"].mode()[0])
df_clean["Ship Date"] = df_clean["Ship Date"].fillna(df_clean["Order Date"])

for col in df_clean.select_dtypes(include="object").columns:
    df_clean[col] = df_clean[col].fillna("Unknown")

df_clean["Sales"] = df_clean["Sales"].fillna(df_clean["Sales"].median())
df_clean["Quantity"] = df_clean["Quantity"].fillna(1)
df_clean["Discount"] = df_clean["Discount"].fillna(0)
df_clean["Profit"] = df_clean["Profit"].fillna(df_clean["Profit"].median())
df_clean["Postal Code"] = df_clean["Postal Code"].fillna(0)

# =========================
# BUSINESS RULE FIX
# =========================
df_clean.loc[df_clean["Ship Date"] < df_clean["Order Date"], "Ship Date"] = df_clean["Order Date"]

# =========================
# CREATE NEW COLUMNS
# =========================
df_clean["Year"] = df_clean["Order Date"].dt.year
df_clean["Month"] = df_clean["Order Date"].dt.month
df_clean["Month Name"] = df_clean["Order Date"].dt.strftime("%b")
df_clean["Quarter"] = "Q" + df_clean["Order Date"].dt.quarter.astype(str)

df_clean["Processing Days"] = (df_clean["Ship Date"] - df_clean["Order Date"]).dt.days

df_clean["Profit Margin %"] = np.where(
    df_clean["Sales"] != 0,
    (df_clean["Profit"] / df_clean["Sales"]) * 100,
    0
)

# =========================
# FORMAT DATES (IMPORTANT FIX)
# =========================
df_clean["Order Date"] = df_clean["Order Date"].dt.strftime("%m/%d/%Y")
df_clean["Ship Date"] = df_clean["Ship Date"].dt.strftime("%m/%d/%Y")

# =========================
# OUTPUT
# =========================
print("Cleaned shape:", df_clean.shape)
print(df_clean.head())

# =========================
# SAVE FILE (EXCEL BEST)
# =========================
df_clean.to_excel("cleaned_superstore_filled.xlsx", index=False)

print("✅ File saved: cleaned_superstore_filled.xlsx")