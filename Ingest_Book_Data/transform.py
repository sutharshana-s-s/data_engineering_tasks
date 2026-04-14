import pandas as pd
import os
import traceback
from datetime import datetime

INPUT_FILE = 'new_data/raw/books/ingest.json'
OUTPUT_DIR = 'new_data/transformed/books/'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'books_transformed.csv')
BASE_URL = "http://books.toscrape.com/catalogue/"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# Transforms book data and saves the cleaned output to a CSV file.
def transform_books():
    print("Starting book data transformation")
    try:
        if not os.path.exists(INPUT_FILE):
            print("Input file not found.")
            return

        df = pd.read_json(INPUT_FILE)

        df['price'] = df['price'].str.replace(r'[^\d.]', '', regex=True).astype(float)
        df['rating'] = df['rating'].map(RATING_MAP).fillna(0).astype(int)
        df['availability'] = df['availability'].apply(lambda x: 1 if str(x).strip().lower() == "in stock" else 0)
        df['book_id'] = df['link'].str.extract(r'_(\d+)/').astype(int)
        df['url'] = df['link'].apply(lambda x: BASE_URL + x.split('../')[-1])
        df['ingestion_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        final_cols = ['book_id', 'title', 'price', 'rating', 'availability', 'url', 'page_metadata', 'ingestion_time']
        df = df[final_cols]

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Transformation successful. Saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error during book transformation: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    transform_books()