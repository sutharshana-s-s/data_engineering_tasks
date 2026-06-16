class Config:
    # Data source
    SOURCE_DIRECTORY = "/Volumes/e_commerce_data/quickstart_schema/sandbox/TASK 4/"
    FILE_EXTENSION = ".csv"
    
    # File parsing - pattern: us-shein-{category_name}-{id}.csv
    FILENAME_PREFIX_PARTS_TO_REMOVE = 2
    FILENAME_SUFFIX_PARTS_TO_REMOVE = 1
    
    # Numeric columns to preserve during schema alignment
    NUMERIC_COLUMNS = {
        "price_usd", 
        "pct_discount", 
        "qty_sold", 
        "rank_number", 
        "category_name"
    }
    
    # Columns to drop after transformation
    COLUMNS_TO_DROP = [
        "price", 
        "discount", 
        "selling_proposition", 
        "rank_title", 
        "rank_sub",
        "goods_title_link", 
        "goods_title_link__jump", 
        "goods_title_link__jump_href",
        "blackfridaybelts_bg_src", 
        "blackfridaybelts_content", 
        "product_locatelabels_img_src"
    ]
    
    # Fill null values for numeric columns
    NUMERIC_FILLNA_COLUMNS = {
        "price_usd": 0.0,
        "pct_discount": 0,
        "qty_sold": 0.0,
        "rank_number": 0
    }
    
    # Regex patterns for data cleaning
    QUANTITY_PREFIX_PATTERN = r"(?i)^\d+\s*(pc|pcs|piece|pieces|mode|modes|in|pack)?[s]?[/]?(\d*(pc|pcs))?\s*[-+/]*\s*(set)?\s*"
    FILLER_WORDS_PATTERN = r"(?i)\s+(with|for|suitable|equipped|made).*$"
    RANK_PREFIX_PATTERN = r"^in "
    
    # Display settings
    SAMPLE_SIZE_FOR_DISPLAY = 10
    MAX_PRODUCT_NAME_LENGTH = 60
