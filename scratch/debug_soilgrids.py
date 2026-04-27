import requests
import json

def debug_soil_grids():
    base_url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
    params = {
        'lon': 78.4867, # Hyderabad
        'lat': 17.3850,
        'property': 'phh2o',
        'depth': '0-5cm',
        'value': 'mean'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        print(f"Status Code: {response.status_code}")
        print("Response Content:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_soil_grids()
