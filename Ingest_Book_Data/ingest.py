import os
import json
import re
import logging
from datetime import datetime

# Configuration
INPUT_DIR = 'Ingest/data/raw/books/2026-04-01/'  # Based on your screenshot path
OUTPUT_DIR = 'new_data/raw/books/'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'ingest.json')

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def ingest_books():
    all_books = []
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(INPUT_DIR):
        logging.error(f"Directory not found: {INPUT_DIR}")
        return

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(INPUT_DIR, filename)
            
            # Extract page number (e.g., data_page_1.json -> 1)
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
                continue

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_books, f, indent=4)
    
    logging.info(f"Ingested {len(all_books)} records into {OUTPUT_FILE}")

if __name__ == "__main__":
    ingest_books()