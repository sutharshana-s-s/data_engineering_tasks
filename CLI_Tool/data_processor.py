import os
import pandas as pd


class DataProcessor:
    @staticmethod
    def _load_data(filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        ext = filepath.split('.')[-1].lower()
        if ext == 'csv':
            return pd.read_csv(filepath)
        elif ext == 'json':
            return pd.read_json(filepath)
        else:
            raise ValueError("Unsupported file format. Please use .csv or .json")

    @classmethod
    def ingest(cls, filepath):
        try:
            df = cls._load_data(filepath)
            print("\n" + "="*60)
            print(f"DATA INGESTION REPORT: {filepath}")
            print("="*60)
            print(f"\nTotal Records: {len(df)}")
            print(f"Total Columns: {len(df.columns)}\n")
            print("Column Names and Data Types:")
            for col in df.columns:
                dtype = str(df[col].dtype)
                print(f"  - {col}: {dtype}")
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"\nERROR: Failed to ingest data - {e}\n")

    @classmethod
    def validate(cls, filepath):
        try:
            df = cls._load_data(filepath)
            print("\n" + "="*60)
            print(f"DATA VALIDATION REPORT: {filepath}")
            print("="*60)
            
            print("\n1. MISSING VALUES ANALYSIS:")
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if not missing.empty:
                for col, cnt in missing.items():
                    pct = (cnt / len(df)) * 100
                    print(f"   {col}: {cnt} ({pct:.2f}%)")
            else:
                print("   No missing values detected")

            print("\n2. DUPLICATE RECORDS ANALYSIS:")
            dups = df.duplicated().sum()
            if dups > 0:
                print(f"   Found {dups} duplicate record(s)")
            else:
                print("   No duplicates detected")

            print("\n3. DATA TYPE CONSISTENCY CHECK:")
            has_issues = False
            for col in df.columns:
                if df[col].dtype == 'object':
                    types = df[col].dropna().apply(type).unique()
                    if len(types) > 1:
                        names = [t.__name__ for t in types]
                        print(f"   Column '{col}': Mixed types detected - {names}")
                        has_issues = True
            if not has_issues:
                print("   All columns have consistent data types")
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"\nERROR: Validation failed - {e}\n")

    @classmethod
    def transform(cls, input_filepath, output_filepath):
        try:
            df = cls._load_data(input_filepath)
            print("\n" + "="*60)
            print("DATA TRANSFORMATION IN PROGRESS")
            print("="*60 + "\n")
            
            df.columns = df.columns.str.strip().str.lower().str.replace(r'\s+', '_', regex=True)
            print("✓ Column names standardized and normalized.")
            
            init_rows = len(df)
            df = df.drop_duplicates()
            dups_removed = init_rows - len(df)
            print(f"✓ Removed {dups_removed} duplicate record(s).")
            
            null_cnt = df.isnull().sum().sum()
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna("Unknown")
            print(f"✓ Processed {null_cnt} missing value(s).")

            out_ext = output_filepath.split('.')[-1].lower()
            if out_ext == 'csv':
                df.to_csv(output_filepath, index=False)
            elif out_ext == 'json':
                df.to_json(output_filepath, orient='records', indent=4)
            else:
                raise ValueError("Output file must be .csv or .json")
            print(f"\n✓ TRANSFORMATION COMPLETE")
            print(f"Output saved: {output_filepath}")
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"\nERROR: Transformation failed - {e}\n")
