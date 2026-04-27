import os
import sys
import django

# Setup Django environment
sys.path.append('/Users/vikasreddy/CropRecommendation')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_recommendation.settings')
django.setup()

from apps.soil.services import SoilDataService

def test_bhuvan_api():
    # Hyderabad coordinates
    lat = 17.3850
    lon = 78.4867
    
    print(f"Testing Bhuvan API with lat={lat}, lon={lon}...")
    data = SoilDataService.fetch_bhuvan_data(lat, lon)
    
    if data:
        print("Bhuvan API returned data:")
        print(data)
    else:
        print("Bhuvan API failed to return data.")

if __name__ == "__main__":
    test_bhuvan_api()
