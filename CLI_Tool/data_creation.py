import pandas as pd
import numpy as np
import random
 
def create_messy_datasets():
    print("Generating base data...")
    num_rows = 5000
   
    # 1. Create Base Data with intentionally messy column names
    data = {
        ' User Name ': [f"User_AB{random.randint(1000, 9999)}" for _ in range(num_rows)],
        'Age': [random.randint(18, 65) for _ in range(num_rows)],
        'Account Balance ': [round(random.uniform(100.0, 5000.0), 2) for _ in range(num_rows)],
        'Status': [random.choice([200, 404, 500]) for _ in range(num_rows)]
    }
    df = pd.DataFrame(data)
 
    print("Injecting discrepancies (Nulls, Mixed Types, Duplicates)...")
   
    # 2. Inject Null / Missing Values
    # Set 10% of 'Age' to NaN
    df.loc[df.sample(frac=0.10).index, 'Age'] = np.nan
    # Set 5% of ' User Name ' to NaN
    df.loc[df.sample(frac=0.05).index, ' User Name '] = np.nan
 
    # 3. Inject Inconsistent Data Types
    # Change 5% of 'Status' (which are ints) to strings
    mixed_indices = df.sample(frac=0.05).index
    df.loc[mixed_indices, 'Status'] = random.choices(["Error", "OK", "Pending"], k=len(mixed_indices))
 
    # 4. Inject Duplicate Rows
    # Pick 250 random rows and append them to the end
    duplicates = df.sample(n=250)
    df = pd.concat([df, duplicates], ignore_index=True)
   
    # Shuffle the dataset so duplicates aren't all clustered at the bottom
    df = df.sample(frac=1).reset_index(drop=True)
 
    print("Saving files...")
    # 5. Save to CSV (Full ~5250 rows)
    csv_file = 'messy_dataset.csv'
    df.to_csv(csv_file, index=False)
   
    # 6. Save a subset to JSON (~2500 rows)
    json_file = 'messy_dataset.json'
    df.head(2500).to_json(json_file, orient='records', indent=4)
 
    print("-" * 40)
    print(f"Success! Created '{csv_file}' ({len(df)} rows)")
    print(f"Success! Created '{json_file}' (2500 rows)")
    print("-" * 40)
    print("Test them in your CLI tool with:")
    print(f"datatool> validate {csv_file}")
    print(f"datatool> transform {csv_file} clean_output.csv")
 
if __name__ == "__main__":
    create_messy_datasets()