# ================================
# 📌 1. IMPORT LIBRARIES
# ================================
import pandas as pd
import numpy as np

# ================================
# 📌 2. LOAD DATASET
# ================================
# 👉 Use your correct file path here
df = pd.read_csv("D:/Internship/labmentix/Real_Estate/data/india_housing_prices.csv")

# ================================
# 📌 3. BASIC DATA CHECKS
# ================================
print(df.head())              # show first 5 rows
print(df.info())              # check data types & nulls
print(df.describe())          # summary stats
print(df.isnull().sum())      # check missing values

# ================================
# 📌 4. DATA CLEANING
# ================================
df = df.drop_duplicates()     # remove duplicate rows

# fill missing numeric values with median
num_cols = df.select_dtypes(include=np.number).columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

# fill missing categorical values with mode
cat_cols = df.select_dtypes(include='object').columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# ================================
# 📌 5. FEATURE ENGINEERING
# ================================

# ✅ Age of property (newer = better)
df['Age_of_Property'] = 2025 - df['Year_Built']

# ✅ Price per SqFt (recalculate for safety)
df['Price_per_SqFt'] = (df['Price_in_Lakhs'] * 100000) / df['Size_in_SqFt']

# ✅ City average price (used later for scoring)
city_avg_price = df.groupby('City')['Price_in_Lakhs'].mean().to_dict()

# ================================
# 🚨 FIX: Convert text → numeric for transport
# ================================
print(df['Public_Transport_Accessibility'].unique())  # check values

# mapping (adjust if needed based on output)
transport_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

df['Transport_Score'] = df['Public_Transport_Accessibility'].map(transport_map)

# if mapping fails (NaN), fill with average value
df['Transport_Score'] = df['Transport_Score'].fillna(2)

# ================================
# ✅ Amenities count
# ================================
df['Amenities_Count'] = df['Amenities'].apply(lambda x: len(str(x).split(',')))

# ================================
# ✅ Accessibility score (now works correctly)
# ================================
df['Accessibility_Score'] = (
    df['Nearby_Schools'] +
    df['Nearby_Hospitals'] +
    df['Transport_Score']
)

# ================================
# ✅ Size category (optional feature)
# ================================
def size_category(size):
    if size < 800:
        return "Small"
    elif size < 1500:
        return "Medium"
    else:
        return "Large"

df['Size_Category'] = df['Size_in_SqFt'].apply(size_category)

# ================================
# 📌 6. SAVE CLEANED DATA
# ================================
df.to_csv("D:/Internship/labmentix/Real_Estate/data/cleaned_data.csv", index=False)

# ================================
# 📌 7. FINAL CHECK
# ================================
print(df.head())  # verify new columns
print("✅ Data cleaning & feature engineering completed successfully!")
