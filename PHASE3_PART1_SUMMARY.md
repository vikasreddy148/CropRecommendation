# Phase 3 Part 1: Data Collection and Preprocessing - COMPLETE ✅

## Summary

Phase 3 Part 1 has been successfully implemented. The data collection and preprocessing pipeline is now ready to prepare training datasets for ML models. The system can collect real data from the Django database, generate synthetic data when needed, and preprocess everything into ready-to-use training datasets.

---

## Features Implemented

### 1. Data Collection Script ✅
- **File**: `ml_training/scripts/collect_data.py`
- **Class**: `DataCollector`
- **Features**:
  - Collects crop recommendation data from Django models
  - Collects yield prediction data from crop history
  - Extracts soil data (pH, N, P, K, moisture)
  - Extracts weather data (temperature, rainfall, humidity)
  - Extracts location data (latitude, longitude)
  - Handles missing data gracefully
  - Generates data statistics

### 2. Synthetic Data Generator ✅
- **File**: `ml_training/scripts/generate_synthetic_data.py`
- **Class**: `SyntheticDataGenerator`
- **Features**:
  - Generates realistic training data based on crop requirements
  - Creates optimal and suboptimal samples
  - Supports 12 crops (Rice, Wheat, Maize, Cotton, Sugarcane, Potato, Tomato, Onion, Chilli, Groundnut, Soybean, Pigeon Pea)
  - Uses realistic Indian regional coordinates
  - Configurable number of samples per crop
  - Reproducible with random seed

### 3. Data Preprocessing ✅
- **File**: `ml_training/scripts/preprocess_data.py`
- **Class**: `DataPreprocessor`
- **Features**:
  - Data cleaning and validation
  - Feature engineering:
    - Nutrient ratios (N/P, N/K, P/K)
    - Total nutrients
    - pH categories
    - Temperature categories
    - Rainfall categories
    - Nutrient sufficiency indicators
    - Location normalization
  - Train/validation/test splitting
  - Feature scaling (StandardScaler)
  - Label encoding (for classification)
  - Saves scalers and encoders for inference

### 4. Main Pipeline Script ✅
- **File**: `ml_training/scripts/data_pipeline.py`
- **Function**: `run_data_pipeline()`
- **Features**:
  - Orchestrates entire pipeline
  - Collects real data from database
  - Generates synthetic data if needed
  - Combines real and synthetic data
  - Preprocesses and saves processed datasets
  - Command-line interface with options
  - Comprehensive error handling

---

## File Structure

```
ml_training/
├── data/                          # Data directory (created automatically)
│   ├── crop_recommendation_raw.csv
│   ├── crop_recommendation_synthetic.csv
│   ├── yield_prediction_raw.csv
│   ├── yield_prediction_synthetic.csv
│   ├── crop_recommendation_X_train.npy
│   ├── crop_recommendation_X_val.npy
│   ├── crop_recommendation_X_test.npy
│   ├── crop_recommendation_y_train.npy
│   ├── crop_recommendation_y_val.npy
│   ├── crop_recommendation_y_test.npy
│   ├── crop_recommendation_scaler.pkl
│   ├── crop_recommendation_encoder.pkl
│   ├── crop_recommendation_metadata.json
│   └── (similar files for yield_prediction)
├── models/                        # For trained models (Phase 3 Part 2)
├── notebooks/                     # For exploration notebooks
├── scripts/
│   ├── __init__.py
│   ├── collect_data.py           # Data collection from Django
│   ├── generate_synthetic_data.py # Synthetic data generation
│   ├── preprocess_data.py        # Data preprocessing
│   └── data_pipeline.py          # Main pipeline script
└── README.md                      # Documentation
```

---

## Usage

### Run Complete Pipeline

```bash
# From project root
python ml_training/scripts/data_pipeline.py
```

### Command-Line Options

```bash
# Skip real data collection
python ml_training/scripts/data_pipeline.py --no-real-data

# Skip synthetic data generation
python ml_training/scripts/data_pipeline.py --no-synthetic-data

# Customize parameters
python ml_training/scripts/data_pipeline.py \
    --min-samples 200 \
    --synthetic-samples 100
```

### Run Individual Steps

```bash
# Collect real data
python ml_training/scripts/collect_data.py

# Generate synthetic data
python ml_training/scripts/generate_synthetic_data.py

# Preprocess data
python ml_training/scripts/preprocess_data.py
```

---

## Data Features

### Crop Recommendation Dataset

**Input Features** (15-18 features):
- `ph`: Soil pH level
- `moisture`: Soil moisture percentage
- `n`: Nitrogen content (kg/ha)
- `p`: Phosphorus content (kg/ha)
- `k`: Potassium content (kg/ha)
- `temperature`: Temperature (°C)
- `rainfall`: Rainfall (mm)
- `humidity`: Humidity (%)
- `np_ratio`: Nitrogen/Phosphorus ratio
- `nk_ratio`: Nitrogen/Potassium ratio
- `pk_ratio`: Phosphorus/Potassium ratio
- `total_nutrients`: Sum of N, P, K
- `n_sufficient`: Binary indicator (N >= 100)
- `p_sufficient`: Binary indicator (P >= 30)
- `k_sufficient`: Binary indicator (K >= 50)
- `lat_norm`: Normalized latitude
- `lon_norm`: Normalized longitude
- `ph_category_encoded`: pH category (acidic/neutral/alkaline)
- `temp_category_encoded`: Temperature category
- `rainfall_category_encoded`: Rainfall category

**Target**:
- `crop_name`: Crop to recommend (12 classes)

### Yield Prediction Dataset

**Input Features**:
- All features from crop recommendation
- `crop_encoded`: Encoded crop type

**Target**:
- `yield_achieved`: Yield in kg/hectare (continuous)

---

## Data Statistics

After running the pipeline, check metadata files for:
- Number of training/validation/test samples
- Number of features
- Number of classes (for classification)
- Feature names
- Class names (for classification)
- Yield statistics (min, max, mean, std)

---

## Data Quality

### Cleaning Steps
- Removes rows with missing critical features
- Validates pH range (0-14)
- Validates nutrient values (non-negative)
- Validates moisture (0-100%)
- Validates temperature range
- Fills missing optional features with defaults

### Feature Engineering
- Creates nutrient ratios for better model understanding
- Categorizes continuous variables (pH, temperature, rainfall)
- Normalizes location coordinates
- Creates binary indicators for nutrient sufficiency

### Data Splitting
- **Train**: 72% (for training models)
- **Validation**: 8% (for hyperparameter tuning)
- **Test**: 20% (for final evaluation)
- Stratified splitting for classification tasks

---

## Output Files

### Raw Data Files
- `crop_recommendation_raw.csv` - Real data from database
- `crop_recommendation_synthetic.csv` - Generated synthetic data
- `yield_prediction_raw.csv` - Real yield data
- `yield_prediction_synthetic.csv` - Generated yield data

### Processed Data Files
- `*_X_train.npy` - Training features (numpy array)
- `*_X_val.npy` - Validation features
- `*_X_test.npy` - Test features
- `*_y_train.npy` - Training targets
- `*_y_val.npy` - Validation targets
- `*_y_test.npy` - Test targets
- `*_scaler.pkl` - Feature scaler (for inference)
- `*_encoder.pkl` - Label encoder (for inference)
- `*_metadata.json` - Dataset metadata

---

## Integration with Django

The data collection script integrates with Django models:
- `apps.farms.models.Field` - Field data
- `apps.farms.models.CropHistory` - Crop history
- `apps.soil.models.SoilData` - Soil measurements
- `apps.weather.models.WeatherData` - Weather data
- `apps.farms.models.Farm` - Farm location

---

## Synthetic Data Generation

When real data is insufficient, the system generates synthetic data based on:
- Known crop requirements (pH, nutrients, temperature, etc.)
- Realistic value ranges
- Optimal and suboptimal condition samples
- Indian regional coordinates
- Seasonal variations

This ensures sufficient training data even with limited real-world data.

---

## Next Steps

After completing Phase 3 Part 1:

1. **Review Data Quality** ✅
   - Check data statistics
   - Verify feature distributions
   - Ensure class balance (for classification)

2. **Phase 3 Part 2: Model Training** ⏭️
   - Train crop recommendation model (classification)
   - Train yield prediction model (regression)
   - Evaluate model performance
   - Save trained models

3. **Phase 3 Part 3: Model Integration** ⏭️
   - Integrate models with Django
   - Update recommendation service to use ML models
   - Add model inference endpoints
   - Update UI to show ML-based recommendations

---

## Testing

### Manual Testing

1. **Run Pipeline**:
   ```bash
   python ml_training/scripts/data_pipeline.py
   ```

2. **Verify Output Files**:
   - Check that all output files are created
   - Verify file sizes are reasonable
   - Check metadata files for correct information

3. **Inspect Data**:
   ```python
   import pandas as pd
   import numpy as np
   
   # Load raw data
   df = pd.read_csv('ml_training/data/crop_recommendation_synthetic.csv')
   print(df.head())
   print(df.describe())
   
   # Load processed data
   X_train = np.load('ml_training/data/crop_recommendation_X_train.npy')
   y_train = np.load('ml_training/data/crop_recommendation_y_train.npy')
   print(f"X_train shape: {X_train.shape}")
   print(f"y_train shape: {y_train.shape}")
   ```

---

## Known Limitations

1. **Real Data Dependency**: 
   - Requires Django database with actual data
   - Falls back to synthetic data if insufficient

2. **Synthetic Data Quality**:
   - Based on known requirements, not real patterns
   - May not capture all real-world variations

3. **Feature Engineering**:
   - Current features are basic
   - Can be extended with domain knowledge

4. **Data Validation**:
   - Basic validation rules
   - Can be enhanced with more sophisticated checks

---

## Status: ✅ COMPLETE

Phase 3 Part 1 is complete with:
- ✅ Data collection from Django database
- ✅ Synthetic data generation
- ✅ Data preprocessing and cleaning
- ✅ Feature engineering
- ✅ Train/val/test splitting
- ✅ Data saving and metadata
- ✅ Command-line interface
- ✅ Documentation

The system is ready for Phase 3 Part 2: Model Training!

---

## Files Created

1. `ml_training/scripts/collect_data.py` - Data collection
2. `ml_training/scripts/generate_synthetic_data.py` - Synthetic data generation
3. `ml_training/scripts/preprocess_data.py` - Data preprocessing
4. `ml_training/scripts/data_pipeline.py` - Main pipeline
5. `ml_training/scripts/__init__.py` - Package init
6. `ml_training/README.md` - Documentation
7. `PHASE3_PART1_SUMMARY.md` - This file

---

## Usage Example

```python
# Run the complete pipeline
from ml_training.scripts.data_pipeline import run_data_pipeline

run_data_pipeline(
    use_real_data=True,
    use_synthetic_data=True,
    min_real_samples=100,
    synthetic_samples_per_crop=50
)
```

Or from command line:

```bash
python ml_training/scripts/data_pipeline.py
```

---

**Phase 3 Part 1: Data Collection and Preprocessing - COMPLETE! ✅**

Ready to proceed with Phase 3 Part 2: Model Training.

