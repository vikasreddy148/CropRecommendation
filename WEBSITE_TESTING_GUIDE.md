# Website Testing Guide - AI/ML Recommendations

Quick guide to test AI/ML recommendations on the website.

---

## Step 1: Access the Website

1. **Make sure Django server is running**:
   ```bash
   python manage.py runserver
   ```

2. **Open your browser**:
   - Go to: **http://127.0.0.1:8000**
   - Or: **http://localhost:8000**

---

## Step 2: Login

1. **If you have an account**: Login with your credentials
2. **If you don't have an account**: 
   - Click "Register" or go to: http://127.0.0.1:8000/register/
   - Create a new account

---

## Step 3: Create Test Data (If Needed)

### Option A: Via Admin Panel (Easiest)

1. **Access Admin**: http://127.0.0.1:8000/admin/
2. **Create Superuser** (if not already created):
   ```bash
   python manage.py createsuperuser
   ```
3. **In Admin Panel**:
   - Go to **Farms** → Add a Farm
     - Name: "Test Farm"
     - Latitude: 20.0
     - Longitude: 77.0
     - Area: 10 hectares
   - Go to **Fields** → Add a Field
     - Farm: Select your farm
     - Name: "Test Field"
     - Soil pH: 6.5
     - Nitrogen (N): 120 kg/ha
     - Phosphorus (P): 30 kg/ha
     - Potassium (K): 50 kg/ha
     - Moisture: 60%
   - (Optional) Go to **Weather Data** → Add Weather Data
     - Latitude: 20.0
     - Longitude: 77.0
     - Temperature: 25°C
     - Rainfall: 600 mm
     - Humidity: 70%

### Option B: Via Website UI

1. **Go to Farms**: http://127.0.0.1:8000/farms/
2. **Create a Farm** with location
3. **Add a Field** with soil data

---

## Step 4: Get AI/ML Recommendations

### Method 1: Request Recommendations Page

1. **Go to Recommendations**:
   - URL: http://127.0.0.1:8000/recommendations/request/
   - Or click "Get Recommendations" from dashboard

2. **Select Your Field**:
   - Choose the field you created
   - Optionally include weather data
   - Click "Get Recommendations"

3. **View Results**:
   - You'll see AI-powered recommendations
   - Each recommendation shows:
     - Crop name
     - Confidence score (from ML model)
     - Expected yield (from ML yield prediction)
     - Profit margin
     - Sustainability score

### Method 2: From Field Detail Page

1. **Go to Your Field**:
   - Navigate to: http://127.0.0.1:8000/farms/fields/
   - Click on your field

2. **Click "Get Recommendations"** button

3. **View Results** immediately

---

## Step 5: Verify AI/ML is Being Used

### Check the Recommendations

Look for these indicators that AI/ML is working:

1. **Confidence Scores**: Should be percentage values (e.g., 75%, 60%)
2. **Yield Predictions**: Should vary based on conditions
3. **Different Recommendations**: Should change for different soil types

### Check in Browser Console (Optional)

1. **Open Developer Tools**: Press `F12` or `Cmd+Option+I` (Mac)
2. **Go to Network Tab**
3. **Request a recommendation**
4. **Check the response** - it should contain recommendation data

### Visual Indicators

- Recommendations are displayed in cards
- Confidence scores shown as progress bars
- Yield and profit displayed for each crop
- Top recommendations sorted by confidence

---

## Expected Results

### When AI/ML is Working:

✅ **Top Recommendations**:
- Wheat: ~75% confidence
- Rice: ~6% confidence  
- Cotton: ~9% confidence
- (Varies based on soil conditions)

✅ **Yield Predictions**:
- Rice: ~3,000-4,000 kg/ha
- Wheat: ~3,200-3,500 kg/ha
- (Realistic values based on conditions)

✅ **Confidence Scores**:
- Range from 0-100%
- Higher scores = better match

---

## Troubleshooting

### No Recommendations Showing

**Check:**
1. Field has soil data (pH, N, P, K)
2. You're logged in
3. Field belongs to your account

**Solution**: Add soil data to your field

### Recommendations Seem Wrong

**Possible causes:**
- Missing soil data
- Unusual soil values
- Weather data mismatch

**Solution**: 
- Verify soil data is correct
- Check field location matches weather data

### Want to Test Different Conditions

**Create multiple fields** with different soil properties:
- Field 1: pH 5.5 (acidic) → Should recommend Rice
- Field 2: pH 7.0 (neutral) → Should recommend Wheat
- Field 3: pH 8.0 (alkaline) → Different recommendations

---

## Quick Test URLs

- **Home/Dashboard**: http://127.0.0.1:8000/
- **Request Recommendations**: http://127.0.0.1:8000/recommendations/request/
- **View All Recommendations**: http://127.0.0.1:8000/recommendations/
- **Farms**: http://127.0.0.1:8000/farms/
- **Fields**: http://127.0.0.1:8000/farms/fields/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## What You Should See

### Recommendation Results Page

- **Card Layout**: Each crop in a card
- **Confidence Bar**: Visual progress bar showing confidence
- **Crop Details**:
  - Crop name
  - Confidence percentage
  - Expected yield (kg/ha)
  - Profit (₹)
  - Sustainability score
- **Top 5-10 Recommendations**: Sorted by confidence

### Example Output

```
Top Recommendation: Wheat
Confidence: 75%
Expected Yield: 3,236 kg/ha
Profit: ₹55,483
Sustainability: 80%
```

---

## Success Indicators

✅ **AI/ML is Working If**:
- Recommendations appear
- Confidence scores are shown
- Yield predictions are realistic
- Different fields give different recommendations
- Recommendations make sense for the soil conditions

---

**Ready to Test!** 🚀

Open http://127.0.0.1:8000 and start testing your AI-powered crop recommendations!

