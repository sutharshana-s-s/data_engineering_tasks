import pandas as pd
import numpy as np
import random
import traceback
 
# Creates messy datasets with nulls, duplicates, and type inconsistencies and saves CSV and JSON files.
def create_messy_datasets():
    print("Starting creation of messy datasets")
    try:
        num_rows = 5000
   
        data = {
            ' User Name ': [f"User_AB{random.randint(1000, 9999)}" for _ in range(num_rows)],
            'Age': [random.randint(18, 65) for _ in range(num_rows)],
            'Account Balance ': [round(random.uniform(100.0, 5000.0), 2) for _ in range(num_rows)],
            'Status': [random.choice([200, 404, 500]) for _ in range(num_rows)]
        }
        df = pd.DataFrame(data)
 
        df.loc[df.sample(frac=0.10).index, 'Age'] = np.nan
        df.loc[df.sample(frac=0.05).index, ' User Name '] = np.nan
 
        mixed_indices = df.sample(frac=0.05).index
        df.loc[mixed_indices, 'Status'] = random.choices(["Error", "OK", "Pending"], k=len(mixed_indices))
 
        duplicates = df.sample(n=250)
        df = pd.concat([df, duplicates], ignore_index=True)
   
        df = df.sample(frac=1).reset_index(drop=True)
 
        csv_file = 'messy_dataset.csv'
        df.to_csv(csv_file, index=False)
   
        json_file = 'messy_dataset.json'
        df.head(2500).to_json(json_file, orient='records', indent=4)
 
        print(f"{'-' * 40}\nSuccess! Created '{csv_file}' ({len(df)} rows)\nSuccess! Created '{json_file}' (2500 rows)\n{'-' * 40}\nTest them in your CLI tool with:\ndatatool> validate {csv_file}\ndatatool> transform {csv_file} clean_output.csv")
    except Exception as e:
        print(f"Error creating messy datasets: {e}")
        traceback.print_exc()
 
if __name__ == "__main__":
    create_messy_datasets()