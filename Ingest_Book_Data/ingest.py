import os
import json
import re
import logging
import traceback
from datetime import datetime

INPUT_DIR = 'Ingest/data/raw/books/2026-04-01/'
OUTPUT_DIR = 'new_data/raw/books/'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'ingest.json')

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Ingests book data from JSON files and writes the combined output to a JSON file.
def ingest_books():
    print("Starting book ingestion")
    try:
        all_books = []
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        if not os.path.exists(INPUT_DIR):
            logging.error(f"Directory not found: {INPUT_DIR}")
            return

        for filename in os.listdir(INPUT_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(INPUT_DIR, filename)
                
                page_match = re.search(r'page_(\d+)', filename)
                page_num = int(page_match.group(1)) if page_match else None

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for record in data:
                            record['page_metadata'] = page_num
                            all_books.append(record)
                except Exception as e:
                    logging.warning(f"Skipping {filename} due to error: {e}")
                    traceback.print_exc()
                    continue

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_books, f, indent=4)

        logging.info(f"Ingested {len(all_books)} records into {OUTPUT_FILE}")
        print(f"Ingested {len(all_books)} records into {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error during book ingestion: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    ingest_books()