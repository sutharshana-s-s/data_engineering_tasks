import os
import pandas as pd
import traceback


class DataProcessor:
    @staticmethod
    def _load_data(filepath):
        # Loads data from a CSV or JSON file using filepath and returns a pandas DataFrame.
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        ext = filepath.split('.')[-1].lower()
        if ext == 'csv':
            df = pd.read_csv(filepath)
        elif ext == 'json':
            df = pd.read_json(filepath)
        else:
            raise ValueError("Unsupported file format. Please use .csv or .json")
        return df

    @classmethod
    def ingest(cls, filepath):
        # Ingests a dataset and prints metadata for the provided filepath.
        print(f"Starting ingest for {filepath}")
        try:
            df = cls._load_data(filepath)
            report = f"\n{'='*60}\nDATA INGESTION REPORT: {filepath}\n{'='*60}\n\nTotal Records: {len(df)}\nTotal Columns: {len(df.columns)}\n\nColumn Names and Data Types:\n"
            for col in df.columns:
                dtype = str(df[col].dtype)
                report += f"  - {col}: {dtype}\n"
            report += f"\n{'='*60}\n"
            print(report)
        except Exception as e:
            print(f"\nERROR: Failed to ingest data - {e}\n")
            traceback.print_exc()

    @classmethod
    def validate(cls, filepath):
        # Validates dataset quality from the provided filepath and prints the validation report.
        print(f"Starting validation for {filepath}")
        try:
            df = cls._load_data(filepath)
            report = f"\n{'='*60}\nDATA VALIDATION REPORT: {filepath}\n{'='*60}\n\n1. MISSING VALUES ANALYSIS:\n"
            missing = df.isnull().sum()
            missing = missing[missing > 0]
            if not missing.empty:
                for col, cnt in missing.items():
                    pct = (cnt / len(df)) * 100
                    report += f"   {col}: {cnt} ({pct:.2f}%)\n"
            else:
                report += "   No missing values detected\n"

            report += "\n2. DUPLICATE RECORDS ANALYSIS:\n"
            dups = df.duplicated().sum()
            if dups > 0:
                report += f"   Found {dups} duplicate record(s)\n"
            else:
                report += "   No duplicates detected\n"

            report += "\n3. DATA TYPE CONSISTENCY CHECK:\n"
            has_issues = False
            for col in df.columns:
                if df[col].dtype == 'object':
                    types = df[col].dropna().apply(type).unique()
                    if len(types) > 1:
                        names = [t.__name__ for t in types]
                        report += f"   Column '{col}': Mixed types detected - {names}\n"
                        has_issues = True
            if not has_issues:
                report += "   All columns have consistent data types\n"
            report += f"\n{'='*60}\n"
            print(report)
        except Exception as e:
            print(f"\nERROR: Validation failed - {e}\n")
            traceback.print_exc()

    @classmethod
    def transform(cls, input_filepath, output_filepath):
        # Transforms and saves the dataset from input_filepath to output_filepath.
        print(f"Starting transform from {input_filepath} to {output_filepath}")
        try:
            df = cls._load_data(input_filepath)
            report = f"\n{'='*60}\nDATA TRANSFORMATION IN PROGRESS\n{'='*60}\n\n"
            
            df.columns = df.columns.str.strip().str.lower().str.replace(r'\s+', '_', regex=True)
            report += "Column names standardized and normalized.\n"
            
            init_rows = len(df)
            df = df.drop_duplicates()
            dups_removed = init_rows - len(df)
            report += f"Removed {dups_removed} duplicate record(s).\n"
            
            null_cnt = df.isnull().sum().sum()
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna("Unknown")
            report += f"Processed {null_cnt} missing value(s).\n"

            out_ext = output_filepath.split('.')[-1].lower()
            if out_ext == 'csv':
                df.to_csv(output_filepath, index=False)
            elif out_ext == 'json':
                df.to_json(output_filepath, orient='records', indent=4)
            else:
                raise ValueError("Output file must be .csv or .json")
            report += f"\nTRANSFORMATION COMPLETE\nOutput saved: {output_filepath}\n\n{'='*60}\n"
            print(report)
        except Exception as e:
            print(f"\nERROR: Transformation failed - {e}\n")
            traceback.print_exc()
