import os
import sys
import django

# Setup Django environment
sys.path.append('/Users/vikasreddy/CropRecommendation')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_recommendation.settings')
django.setup()

from apps.soil.services import SoilDataService

def test_soil_grids():
    lat = 30.9010 # Ludhiana, Punjab
    lon = 75.8573
    
    print(f"Testing Soil Grids API with lat={lat}, lon={lon}...")
    data = SoilDataService.fetch_soil_grids_data(lat, lon)
    
    if data:
        print("Soil Grids API returned data:")
        for k, v in data.items():
            print(f"  {k}: {v}")
    else:
        print("Soil Grids API failed to return data.")

if __name__ == "__main__":
    test_soil_grids()
