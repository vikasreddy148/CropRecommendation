import pandas as pd
import requests
from pathlib import Path

# URL for the Kaggle dataset (hosted on GitHub raw)
URL = "https://raw.githubusercontent.com/Gladiator07/Harvestify/master/Data-processed/crop_recommendation.csv"
OUTPUT_PATH = Path("/Users/vikasreddy/CropRecommendation/ml_training/data/crop_recommendation_raw.csv")

def download_and_format():
    print(f"Downloading data from {URL}...")
    response = requests.get(URL)
    response.raise_for_status()
    
    # Load into pandas
    from io import StringIO
    df = pd.read_csv(StringIO(response.text))
    
    print(f"Downloaded {len(df)} rows.")
    print("Original columns:", df.columns.tolist())
    
    # Format columns: lowercase and rename
    df.columns = [col.lower() for col in df.columns]
    
    # Rename 'label' to 'crop_name' if it exists
    if 'label' in df.columns:
        df = df.rename(columns={'label': 'crop_name'})
        
    print("Formatted columns:", df.columns.tolist())
    
    # Save to crop_recommendation_raw.csv
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    download_and_format()
