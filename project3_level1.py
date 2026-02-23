import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("archive (3)/AB_NYC_2019.csv")

# 1. View basic info
print("Initial Shape:", df.shape)
print(df.info())
print(df.head())

# 2. Remove duplicate rows
df = df.drop_duplicates()
print("After removing duplicates:", df.shape)

# 3. Handle missing values
print("Missing values:\n", df.isnull().sum())

# Option: Fill or drop missing values based on column
df['name'].fillna("Unknown", inplace=True)
df['host_name'].fillna("Unknown", inplace=True)
df.dropna(subset=['latitude', 'longitude', 'price'], inplace=True)  # Critical columns

# 4. Standardize text columns
df['neighbourhood_group'] = df['neighbourhood_group'].str.strip().str.title()
df['room_type'] = df['room_type'].str.strip().str.title()

# 5. Convert 'price' to numeric if necessary
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 6. Detect outliers in price using IQR
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
print("After removing price outliers:", df.shape)

# 7. Check for invalid coordinates
df = df[(df['latitude'].between(-90, 90)) & (df['longitude'].between(-180, 180))]

# 8. Reset index
df.reset_index(drop=True, inplace=True)

# 9. Summary
print("Final dataset shape:", df.shape)
print(df.describe(include='all'))

# Optional: Save cleaned data
df.to_csv("cleaned_dataset.csv", index=False)

# Optional: Visualize price distribution
plt.figure(figsize=(10, 5))
sns.histplot(df['price'], bins=50, kde=True)
plt.title('Price Distribution after Cleaning')
plt.xlabel('Price ($)')
plt.show()
