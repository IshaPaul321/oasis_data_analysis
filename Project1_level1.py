import pandas as pd
import numpy as np
import os
import json

# ✅ Define country codes for loop
country_codes = ['US', 'IN', 'CA', 'DE', 'FR', 'GB', 'JP', 'KR', 'MX', 'RU']
for code in country_codes:
    csv_file = f"{code}videos.csv"
    json_file = f"{code}_category_id.json"

    if os.path.exists(csv_file) and os.path.exists(json_file):
        print(f"Processing {csv_file}...")

        # Load CSV
        try:
            df = pd.read_csv(csv_file)
            print(f"✅ Loaded {csv_file} with shape: {df.shape}")
        except Exception as e:
            print(f"❌ Error loading {csv_file}: {e}")
            continue  # <--- This continue is inside the for loop

        # Clean
        try:
            df = clean_dataset(df)
            print(f"✅ Cleaned {code} dataset with shape: {df.shape}")
        except Exception as e:
            print(f"❌ Error cleaning {csv_file}: {e}")
            continue

        # Category mapping
        try:
            cat_map = load_category_mapping(json_file)
            df['category_name'] = df['category_id'].map(cat_map)
            print(f"✅ Category mapping complete for {code}")
        except Exception as e:
            print(f"❌ Error mapping categories for {code}: {e}")
            continue

        # Save
        try:
            output_file = f"cleaned_{code}.csv"
            df.to_csv(output_file, index=False)
            print(f"✅ Saved cleaned data to {output_file}\n")
        except Exception as e:
            print(f"❌ Error saving file {output_file}: {e}")
            continue
    else:
        print(f"⚠️ Missing files for {code}. Skipping...\n")
