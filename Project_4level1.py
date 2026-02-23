import pandas as pd

# Load the Excel file
file_path = 'DEvideos.csv'  # Update this to your actual file name
df = pd.read_csv(file_path)

print("🔹 Original Dataset Shape:", df.shape)

# Drop duplicate rows
df.drop_duplicates(inplace=True)
print("✅ After removing duplicates:", df.shape)

# Drop rows with missing essential fields
required_columns = [
    'video_id', 'title', 'channel_title', 'publish_time',
    'views', 'likes', 'dislikes', 'comment_count'
]
df.dropna(subset=required_columns, inplace=True)

# Remove rows with blank strings in required fields
for col in ['video_id', 'title', 'channel_title', 'publish_time']:
    df = df[df[col].astype(str).str.strip() != ""]

print("✅ After removing rows with missing/blank essential fields:", df.shape)

# Convert numeric columns to proper types and drop rows where conversion fails
numeric_columns = ['views', 'likes', 'dislikes', 'comment_count', 'category_id']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # convert invalid to NaN

df.dropna(subset=numeric_columns, inplace=True)

print("✅ After ensuring numeric columns are clean:", df.shape)

# Save the cleaned data
output_file = 'DEvideo_output.csv'
df.to_csv(output_file, index=False)

print(f"🎉 Cleaned dataset saved as '{output_file}'")
