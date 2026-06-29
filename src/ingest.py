import os
import sqlite3
import pandas as pd
import requests

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "zomato.csv")
DB_PATH = os.path.join(DATA_DIR, "zomato.db")
DATASET_URL = "https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation/resolve/main/zomato.csv"

def download_dataset():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

    # Ensure the file exists and is not empty/truncated
    if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 1024 * 1024:
        print(f"Dataset already exists at: {CSV_PATH} and is valid. Skipping download.")
        return

    print(f"Downloading dataset from {DATASET_URL}...")
    try:
        response = requests.get(DATASET_URL, stream=True)
        response.raise_for_status()
        
        with open(CSV_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        raise e

def clean_rating(val):
    if pd.isna(val):
        return 0.0
    val_str = str(val).strip().split("/")[0].strip()
    if val_str in ("NEW", "-", ""):
        return 0.0
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def clean_cost(val):
    if pd.isna(val):
        return 0.0
    val_str = str(val).replace(",", "").strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def normalize_location(val):
    if not val:
        return ""
    val_lower = str(val).lower().strip()
    
    # Map sub-localities to primary parent localities
    if "koramangala" in val_lower:
        return "Koramangala"
    if "whitefield" in val_lower:
        return "Whitefield"
    if "banashankari" in val_lower:
        return "Banashankari"
    if "bellandur" in val_lower:
        return "Bellandur"
    if "btm" in val_lower:
        return "BTM"
    if "hsr" in val_lower:
        return "HSR"
    if "jayanagar" in val_lower:
        return "Jayanagar"
    if "jp nagar" in val_lower:
        return "JP Nagar"
    if "indiranagar" in val_lower:
        return "Indiranagar"
    if "malleshwaram" in val_lower:
        return "Malleshwaram"
    if "rajajinagar" in val_lower:
        return "Rajajinagar"
    if "banaswadi" in val_lower:
        return "Banaswadi"
    if "basavanagudi" in val_lower:
        return "Basavanagudi"
    if "electronic city" in val_lower:
        return "Electronic City"
    if "marathahalli" in val_lower:
        return "Marathahalli"
    if "sarjapur" in val_lower:
        return "Sarjapur Road"
    if "bannerghatta" in val_lower:
        return "Bannerghatta Road"
    if "kalyan nagar" in val_lower:
        return "Kalyan Nagar"
    if "kammanahalli" in val_lower:
        return "Kammanahalli"
    if "new bel road" in val_lower:
        return "New BEL Road"
    if "peenya" in val_lower:
        return "Peenya"
    if "yeshwantpur" in val_lower:
        return "Yeshwantpur"
    if "yelahanka" in val_lower:
        return "Yelahanka"
    if "hebbal" in val_lower:
        return "Hebbal"
    if "hennur" in val_lower:
        return "Hennur"
    if "hbr" in val_lower:
        return "HBR Layout"
    if "rt nagar" in val_lower:
        return "RT Nagar"
    if "sanjay nagar" in val_lower:
        return "Sanjay Nagar"
    if "domlur" in val_lower:
        return "Domlur"
    if "old airport" in val_lower:
        return "Old Airport Road"
    if "shanti nagar" in val_lower:
        return "Shanti Nagar"
    if "vasanth nagar" in val_lower:
        return "Vasanth Nagar"
    if "commercial street" in val_lower:
        return "Commercial Street"
    if "cunningham" in val_lower:
        return "Cunningham Road"
    if "frazer town" in val_lower:
        return "Frazer Town"
    if "basaveshwara" in val_lower:
        return "Basaveshwara Nagar"
    
    return str(val).title().strip()


def process_and_store():
    print(f"Reading dataset from {CSV_PATH}...")
    # Read CSV. Since Zomato CSV can have quote and comma issues, we use low_memory=False
    df = pd.read_csv(CSV_PATH, low_memory=False)
    print(f"Loaded {len(df)} records.")
    print("Columns in dataset:", df.columns.tolist())

    # Preprocessing columns as per architecture spec
    # Clean ratings: extract float from formats like "4.1/5"
    print("Cleaning rating column...")
    df['rating_clean'] = df['rate'].apply(clean_rating)

    # Clean approx cost: remove commas and parse as float
    print("Cleaning cost column...")
    # Find matching column for cost (could be approx_cost(for two people) or similar)
    cost_col = [col for col in df.columns if 'cost' in col.lower() or 'approx' in col.lower()]
    if cost_col:
        print(f"Found cost column: '{cost_col[0]}'")
        df['cost_clean'] = df[cost_col[0]].apply(clean_cost)
    else:
        print("Warning: Cost column not found. Defaulting clean cost to 0.")
        df['cost_clean'] = 0.0

    # Ensure other critical columns exist
    critical_cols = {
        'name': 'name',
        'location': 'location',
        'cuisines': 'cuisines',
        'address': 'address'
    }
    
    for key, default in critical_cols.items():
        matching = [col for col in df.columns if col.lower() == key]
        if matching:
            df[key] = df[matching[0]].fillna("").astype(str)
        else:
            print(f"Warning: Column '{key}' not found. Initializing with empty strings.")
            df[key] = ""

    # Clean string columns
    df['name'] = df['name'].str.strip()
    df['cuisines'] = df['cuisines'].str.strip()
    df['address'] = df['address'].str.strip()

    # If location is empty/null, fall back to listed_in(city) which contains clean neighborhood names
    if 'listed_in(city)' in df.columns:
        df['location'] = df['location'].replace("", pd.NA).fillna(df['listed_in(city)']).fillna("").astype(str).str.strip()
    else:
        df['location'] = df['location'].fillna("").astype(str).str.strip()

    # Normalize location to primary parent neighborhood
    print("Normalizing location names to main neighborhoods...")
    df['location'] = df['location'].apply(normalize_location)


    # Store into SQLite
    print(f"Saving to SQLite database: {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    
    # Store clean dataset
    # Select columns we want to retain for the recommendation service
    output_cols = ['name', 'address', 'location', 'cuisines', 'rating_clean', 'cost_clean']
    
    # Also carry forward original rate and cost for reference/display if desired
    if cost_col and cost_col[0] in df.columns:
        df['original_cost'] = df[cost_col[0]].fillna("").astype(str)
        output_cols.append('original_cost')
    if 'rate' in df.columns:
        df['original_rate'] = df['rate'].fillna("").astype(str)
        output_cols.append('original_rate')

    # Filter out empty restaurant names and remove duplicates
    df_clean = df[df['name'] != ''][output_cols].drop_duplicates(subset=['name', 'address', 'location', 'cuisines'])
    
    df_clean.to_sql("restaurants", conn, if_exists="replace", index=False)
    
    # Create indexes for optimized filtering
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_location ON restaurants(location)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rating ON restaurants(rating_clean)")
    conn.commit()
    conn.close()
    
    print(f"Successfully processed and stored {len(df_clean)} records in SQLite database.")
    print("Database processing completed successfully!")

if __name__ == "__main__":
    try:
        download_dataset()
        process_and_store()
    except Exception as e:
        print(f"Execution failed: {e}")
