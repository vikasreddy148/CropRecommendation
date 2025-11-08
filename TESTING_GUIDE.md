# Testing Guide for AI/ML Recommendations

This guide shows you how to test the crop recommendation system and verify that AI/ML models are being used.

---

## Quick Test Methods

### Method 1: Test via Django Admin/UI (Easiest)

1. **Start Django Server** (if not running):
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Access the Application**:
   - Open browser: http://127.0.0.1:8000
   - Login to your account

3. **Create Test Data** (if needed):
   - Go to Farms → Create a farm
   - Add a field with soil data:
     - pH: 6.5
     - Nitrogen (N): 120 kg/ha
     - Phosphorus (P): 30 kg/ha
     - Potassium (K): 50 kg/ha
     - Moisture: 60%

4. **Request Recommendations**:
   - Go to Recommendations → Request Recommendations
   - Select your field
   - Click "Get Recommendations"

5. **Check Results**:
   - Look at the recommendations displayed
   - Check if they make sense for your soil conditions
   - Verify yield predictions are shown

---

### Method 2: Test via Python Shell (Recommended for Verification)

This method lets you directly verify that ML models are being used.

#### Step 1: Open Django Shell

```bash
source venv/bin/activate
python manage.py shell
```

#### Step 2: Test ML Service Directly

```python
# Import the ML service
from apps.recommendations.ml_service import get_ml_service

# Get ML service instance
ml_service = get_ml_service()

# Check if models are loaded
print("Crop model loaded:", ml_service.crop_model_data is not None)
print("Yield model loaded:", ml_service.yield_model_data is not None)

# Test crop recommendation
recommendations = ml_service.predict_crop_recommendations(
    soil_ph=6.5,
    soil_n=120,
    soil_p=30,
    soil_k=50,
    soil_moisture=60,
    temperature=25,
    rainfall=600,
    humidity=70,
    latitude=20.0,
    longitude=77.0
)

print("\nTop 5 Crop Recommendations:")
for i, rec in enumerate(recommendations[:5], 1):
    print(f"{i}. {rec['crop_name']}: {rec['confidence_score']:.2f}% confidence")

# Test yield prediction
yield_pred = ml_service.predict_yield(
    crop_name='Rice',
    soil_ph=6.5,
    soil_n=120,
    soil_p=30,
    soil_k=50,
    soil_moisture=60,
    temperature=25,
    rainfall=600,
    humidity=70
)

print(f"\nPredicted yield for Rice: {yield_pred:.2f} kg/ha")
```

#### Step 3: Test Full Recommendation Service

```python
# Import the recommendation service
from apps.recommendations.services import CropRecommendationService

# Test with sample data
recommendations = CropRecommendationService.get_recommendations(
    soil_ph=6.5,
    soil_n=120,
    soil_p=30,
    soil_k=50,
    soil_moisture=60,
    temperature=25,
    rainfall=600,
    humidity=70,
    latitude=20.0,
    longitude=77.0,
    limit=5
)

print("\n=== Recommendations ===")
for i, rec in enumerate(recommendations, 1):
    print(f"\n{i}. {rec['crop_name']}")
    print(f"   Confidence: {rec['confidence_score']:.2f}%")
    print(f"   Expected Yield: {rec['expected_yield']:.2f} kg/ha")
    print(f"   Profit: ₹{rec['profit_margin']:.2f}")
    print(f"   ML Prediction: {rec.get('ml_prediction', False)}")
    print(f"   Sustainability: {rec['sustainability_score']}%")
```

#### Step 4: Test with Real Field Data

```python
# Import models
from apps.farms.models import Field
from apps.recommendations.services import CropRecommendationService

# Get a field (replace with your field ID)
field = Field.objects.first()

if field:
    # Get recommendations for the field
    recommendations = CropRecommendationService.get_recommendation_for_field(
        field=field,
        limit=5
    )
    
    print(f"\nRecommendations for {field.name}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['crop_name']}")
        print(f"   Confidence: {rec['confidence_score']:.2f}%")
        print(f"   Using ML: {rec.get('ml_prediction', False)}")
else:
    print("No fields found. Create a field first.")
```

---

### Method 3: Test via Django Views (Web Interface)

1. **Create Test Data via Admin**:
   ```bash
   python manage.py createsuperuser  # if not already created
   python manage.py runserver
   ```
   - Go to http://127.0.0.1:8000/admin
   - Create a Farm
   - Create a Field with soil data
   - Add Weather Data (optional)

2. **Test Recommendations**:
   - Go to http://127.0.0.1:8000/recommendations/request/
   - Select your field
   - Submit the form
   - View results

3. **Check in Browser Console** (if you want to see the data):
   - Open browser developer tools (F12)
   - Check the network tab to see the recommendation data
   - Look for `ml_prediction: true` in the response

---

## Verification Checklist

### ✅ Verify ML Models Are Loaded

```python
from apps.recommendations.ml_service import get_ml_service

ml_service = get_ml_service()
print("Crop model:", "✅ Loaded" if ml_service.crop_model_data else "❌ Not loaded")
print("Yield model:", "✅ Loaded" if ml_service.yield_model_data else "❌ Not loaded")
```

### ✅ Verify ML Models Are Being Used

```python
from apps.recommendations.services import CropRecommendationService

recs = CropRecommendationService.get_recommendations(
    soil_ph=6.5, soil_n=120, soil_p=30, soil_k=50,
    temperature=25, rainfall=600, limit=3
)

# Check if ML is being used
using_ml = any(rec.get('ml_prediction', False) for rec in recs)
print("Using ML models:", "✅ Yes" if using_ml else "❌ No (using rule-based)")

# Show first recommendation
if recs:
    print(f"\nTop recommendation: {recs[0]['crop_name']}")
    print(f"Confidence: {recs[0]['confidence_score']:.2f}%")
    print(f"ML Prediction: {recs[0].get('ml_prediction', False)}")
```

### ✅ Test Different Soil Conditions

```python
# Test acidic soil (good for Rice)
recs_acidic = CropRecommendationService.get_recommendations(
    soil_ph=5.5, soil_n=100, soil_p=20, soil_k=40,
    temperature=28, rainfall=1000, limit=3
)
print("Acidic soil recommendations:")
for rec in recs_acidic:
    print(f"  - {rec['crop_name']}: {rec['confidence_score']:.2f}%")

# Test neutral soil (good for Wheat)
recs_neutral = CropRecommendationService.get_recommendations(
    soil_ph=7.0, soil_n=120, soil_p=30, soil_k=50,
    temperature=20, rainfall=500, limit=3
)
print("\nNeutral soil recommendations:")
for rec in recs_neutral:
    print(f"  - {rec['crop_name']}: {rec['confidence_score']:.2f}%")
```

### ✅ Test Yield Predictions

```python
from apps.recommendations.ml_service import get_ml_service

ml_service = get_ml_service()

# Test yield for different crops
crops = ['Rice', 'Wheat', 'Maize', 'Potato']

for crop in crops:
    yield_pred = ml_service.predict_yield(
        crop_name=crop,
        soil_ph=6.5,
        soil_n=120,
        soil_p=30,
        soil_k=50,
        soil_moisture=60,
        temperature=25,
        rainfall=600
    )
    print(f"{crop}: {yield_pred:.2f} kg/ha")
```

---

## Expected Results

### When ML Models Are Working:

1. **Recommendations should include**:
   - `'ml_prediction': True` in the recommendation dict
   - Reasonable confidence scores (typically 50-95%)
   - Yield predictions that vary based on conditions
   - Different recommendations for different soil types

2. **Yield predictions should**:
   - Be realistic (e.g., Rice: 2000-4000 kg/ha)
   - Vary based on soil conditions
   - Be different for different crops

3. **Django logs should show** (when making recommendations):
   ```
   Using ML model for recommendations. Generated X recommendations.
   ```

### When Using Rule-Based (Fallback):

1. **Recommendations will have**:
   - `'ml_prediction': False`
   - Still work correctly, just using rules instead of ML

---

## Complete Test Script

Save this as `test_recommendations.py` and run it:

```python
#!/usr/bin/env python
"""
Complete test script for AI/ML recommendations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_recommendation.settings')
django.setup()

from apps.recommendations.ml_service import get_ml_service
from apps.recommendations.services import CropRecommendationService

print("=" * 60)
print("Testing AI/ML Crop Recommendations")
print("=" * 60)

# Test 1: Check if models are loaded
print("\n1. Checking ML Models...")
ml_service = get_ml_service()
crop_loaded = ml_service.crop_model_data is not None
yield_loaded = ml_service.yield_model_data is not None

print(f"   Crop Recommendation Model: {'✅ Loaded' if crop_loaded else '❌ Not loaded'}")
print(f"   Yield Prediction Model: {'✅ Loaded' if yield_loaded else '❌ Not loaded'}")

if not (crop_loaded and yield_loaded):
    print("\n⚠️  Models not loaded. Train models first:")
    print("   python ml_training/scripts/train_models.py")
    exit(1)

# Test 2: Test crop recommendations
print("\n2. Testing Crop Recommendations...")
recommendations = CropRecommendationService.get_recommendations(
    soil_ph=6.5,
    soil_n=120,
    soil_p=30,
    soil_k=50,
    soil_moisture=60,
    temperature=25,
    rainfall=600,
    humidity=70,
    latitude=20.0,
    longitude=77.0,
    limit=5
)

using_ml = any(rec.get('ml_prediction', False) for rec in recommendations)
print(f"   Using ML Models: {'✅ Yes' if using_ml else '❌ No (rule-based)'}")

print("\n   Top 5 Recommendations:")
for i, rec in enumerate(recommendations[:5], 1):
    ml_indicator = "🤖" if rec.get('ml_prediction', False) else "📋"
    print(f"   {i}. {ml_indicator} {rec['crop_name']}")
    print(f"      Confidence: {rec['confidence_score']:.2f}%")
    print(f"      Yield: {rec['expected_yield']:.2f} kg/ha")
    print(f"      Profit: ₹{rec['profit_margin']:.2f}")

# Test 3: Test yield prediction
print("\n3. Testing Yield Predictions...")
test_crops = ['Rice', 'Wheat', 'Maize']
for crop in test_crops:
    yield_pred = ml_service.predict_yield(
        crop_name=crop,
        soil_ph=6.5,
        soil_n=120,
        soil_p=30,
        soil_k=50,
        soil_moisture=60,
        temperature=25,
        rainfall=600,
        humidity=70
    )
    print(f"   {crop}: {yield_pred:.2f} kg/ha")

# Test 4: Test with different conditions
print("\n4. Testing Different Soil Conditions...")
conditions = [
    ("Acidic (pH 5.5)", 5.5, 100, 20, 40),
    ("Neutral (pH 7.0)", 7.0, 120, 30, 50),
    ("Alkaline (pH 8.0)", 8.0, 80, 25, 45),
]

for name, ph, n, p, k in conditions:
    recs = CropRecommendationService.get_recommendations(
        soil_ph=ph, soil_n=n, soil_p=p, soil_k=k,
        temperature=25, rainfall=600, limit=1
    )
    if recs:
        print(f"   {name}: {recs[0]['crop_name']} ({recs[0]['confidence_score']:.1f}%)")

print("\n" + "=" * 60)
print("✅ Testing Complete!")
print("=" * 60)
```

Run it:
```bash
python test_recommendations.py
```

---

## Troubleshooting

### Models Not Loading

**Check:**
```bash
ls ml_training/models/*.pkl
```

**If missing, train models:**
```bash
python ml_training/scripts/data_pipeline.py
python ml_training/scripts/train_models.py
```

### Getting Rule-Based Instead of ML

**Check:**
1. Models exist in `ml_training/models/`
2. No errors in Django logs
3. ML service is loading correctly

**Test:**
```python
from apps.recommendations.ml_service import get_ml_service
ml_service = get_ml_service()
print(ml_service.crop_model_data is not None)  # Should be True
```

### Recommendations Seem Wrong

**Possible causes:**
1. Models trained on different data
2. Feature mismatch
3. Need to retrain with better data

**Solution:**
- Retrain models with more/better data
- Check feature preparation matches training

---

## Quick Test Commands

```bash
# Test 1: Check models exist
ls ml_training/models/*.pkl

# Test 2: Run test script
python test_recommendations.py

# Test 3: Django shell test
python manage.py shell
# Then paste the test code from Method 2 above
```

---

**Happy Testing! 🧪**

If you encounter any issues, check the troubleshooting section or review the Django logs for error messages.

