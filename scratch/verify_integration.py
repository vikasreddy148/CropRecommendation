import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_recommendation.settings')
django.setup()

from apps.recommendations.services import CropRecommendationService

def test_recommendations():
    print("Testing CropRecommendationService with new model...")
    
    # Test case 1: Typical rice conditions
    # N=90, P=42, K=43, temp=20.8, hum=82, ph=6.5, rain=202
    results = CropRecommendationService.get_recommendations(
        soil_n=90, soil_p=42, soil_k=43,
        temperature=20.8, humidity=82, soil_ph=6.5, rainfall=202,
        limit=3
    )
    
    print("\nTest Case 1: Rice Conditions")
    for i, rec in enumerate(results):
        print(f"{i+1}. {rec['crop_name']} (Confidence: {rec['confidence_score']}%)")
        print(f"   Expected Yield: {rec['expected_yield']} kg/ha")
        print(f"   Profit Margin: {rec['profit_margin']}")
        print(f"   Sustainability Score: {rec['sustainability_score']}")
        
    # Test case 2: Typical pomegranate conditions
    # N=20, P=10, K=40, temp=25, hum=60, ph=7, rain=150
    results = CropRecommendationService.get_recommendations(
        soil_n=20, soil_p=10, soil_k=40,
        temperature=25, humidity=60, soil_ph=7, rainfall=150,
        limit=3
    )
    
    print("\nTest Case 2: Pomegranate/Fruit Conditions")
    for i, rec in enumerate(results):
        print(f"{i+1}. {rec['crop_name']} (Confidence: {rec['confidence_score']}%)")
        
    # Test case 3: Typical coffee conditions
    # N=100, P=30, K=30, temp=25, hum=60, ph=6.5, rain=140
    results = CropRecommendationService.get_recommendations(
        soil_n=100, soil_p=30, soil_k=30,
        temperature=25, humidity=60, soil_ph=6.5, rainfall=140,
        limit=3
    )
    
    print("\nTest Case 3: Coffee Conditions")
    for i, rec in enumerate(results):
        print(f"{i+1}. {rec['crop_name']} (Confidence: {rec['confidence_score']}%)")

if __name__ == "__main__":
    test_recommendations()
