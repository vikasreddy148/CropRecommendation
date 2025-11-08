# Model Training Guide

This guide explains how to train the ML models for crop recommendation and yield prediction.

---

## Overview

The training process consists of three main steps:

1. **Data Collection and Preprocessing** - Prepare training data
2. **Model Training** - Train ML models on the data
3. **Model Integration** - Models are automatically used by Django

---

## Step-by-Step Training Process

### Step 1: Data Collection and Preprocessing

Before training models, you need to prepare the training data.

#### Option A: Use Synthetic Data (Recommended for First Time)

If you don't have real data yet, generate synthetic training data:

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run data pipeline (generates synthetic data automatically)
python ml_training/scripts/data_pipeline.py
```

This will:
- Generate synthetic training data (600 samples: 50 per crop × 12 crops)
- Preprocess and clean the data
- Create train/validation/test splits
- Save processed data to `ml_training/data/`

#### Option B: Use Real Data from Database

If you have real data in your Django database:

```bash
# Collect real data from database
python ml_training/scripts/collect_data.py

# If you need more data, generate synthetic to supplement
python ml_training/scripts/generate_synthetic_data.py

# Preprocess the data
python ml_training/scripts/preprocess_data.py
```

#### What Gets Created

After data preprocessing, you'll have:

**Raw Data Files** (in `ml_training/data/`):
- `crop_recommendation_raw.csv` or `crop_recommendation_synthetic.csv`
- `yield_prediction_raw.csv` or `yield_prediction_synthetic.csv`

**Processed Data Files**:
- `crop_recommendation_X_train.npy` - Training features
- `crop_recommendation_X_val.npy` - Validation features
- `crop_recommendation_X_test.npy` - Test features
- `crop_recommendation_y_train.npy` - Training labels
- `crop_recommendation_y_val.npy` - Validation labels
- `crop_recommendation_y_test.npy` - Test labels
- `crop_recommendation_scaler.pkl` - Feature scaler
- `crop_recommendation_encoder.pkl` - Label encoder
- `crop_recommendation_metadata.json` - Dataset metadata

Similar files for yield prediction with `yield_prediction_` prefix.

---

### Step 2: Train the Models

Once you have preprocessed data, train the models:

#### Train Both Models (Recommended)

```bash
python ml_training/scripts/train_models.py
```

This will:
1. Check for preprocessed data
2. Train crop recommendation model (classification)
3. Train yield prediction model (regression)
4. Evaluate both models on test set
5. Save trained models and metrics

#### Train Individual Models

**Crop Recommendation Only:**
```bash
python ml_training/scripts/train_crop_recommendation.py
```

**Yield Prediction Only:**
```bash
python ml_training/scripts/train_yield_prediction.py
```

#### Custom Training Parameters

```bash
# Train with custom parameters
python ml_training/scripts/train_models.py \
    --n-estimators 200 \
    --max-depth 10

# Train only yield prediction with gradient boosting
python ml_training/scripts/train_models.py \
    --yield-only \
    --model-type gradient_boosting \
    --n-estimators 150
```

---

### Step 3: Verify Training Success

After training, check the outputs:

#### Check Model Files

```bash
ls ml_training/models/
```

You should see:
- `crop_recommendation_model.pkl` - Trained classifier
- `crop_recommendation_scaler.pkl` - Feature scaler
- `crop_recommendation_encoder.pkl` - Label encoder
- `crop_recommendation_model_metadata.json` - Model info
- `crop_recommendation_metrics.json` - Evaluation metrics
- Similar files for `yield_prediction_`

#### Check Training Metrics

```bash
# View crop recommendation metrics
cat ml_training/models/crop_recommendation_metrics.json

# View yield prediction metrics
cat ml_training/models/yield_prediction_metrics.json
```

**Expected Metrics:**

**Crop Recommendation:**
- Accuracy: 70-90% (depending on data quality)
- F1 Score: 0.70-0.90
- Precision and Recall per crop

**Yield Prediction:**
- RMSE: 10-20% of average yield
- R² Score: 0.60-0.85
- MAE: Similar to RMSE

---

## What Happens During Training

### Crop Recommendation Model (Classification)

1. **Load Data**: Loads preprocessed training/validation/test sets
2. **Train Model**: 
   - Creates Random Forest Classifier
   - Uses 100 trees by default
   - Handles class imbalance with balanced weights
   - Trains on training set
3. **Validate**: Evaluates on validation set during training
4. **Evaluate**: Tests on test set with comprehensive metrics
5. **Save**: Saves model, scaler, encoder, and metadata

**Model Details:**
- **Algorithm**: Random Forest Classifier
- **Input**: 15-18 features (soil, weather, location, engineered)
- **Output**: Crop name (12 classes)
- **Training Time**: 1-5 minutes (depending on data size)

### Yield Prediction Model (Regression)

1. **Load Data**: Loads preprocessed training/validation/test sets
2. **Train Model**:
   - Creates Random Forest Regressor (or Gradient Boosting)
   - Uses 100 trees by default
   - Trains on training set
3. **Validate**: Evaluates on validation set
4. **Evaluate**: Tests on test set with regression metrics
5. **Save**: Saves model, scalers, encoder, and metadata

**Model Details:**
- **Algorithm**: Random Forest Regressor / Gradient Boosting Regressor
- **Input**: 16-19 features (crop type, soil, weather, location)
- **Output**: Yield in kg/hectare (continuous)
- **Training Time**: 1-5 minutes

---

## Complete Training Workflow

Here's the complete workflow from start to finish:

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies (if not already installed)
pip install -r requirements.txt

# 3. Generate and preprocess data
python ml_training/scripts/data_pipeline.py

# 4. Train models
python ml_training/scripts/train_models.py

# 5. Verify models were created
ls ml_training/models/

# 6. Check metrics
cat ml_training/models/crop_recommendation_metrics.json
cat ml_training/models/yield_prediction_metrics.json

# 7. Restart Django (models will be loaded automatically)
python manage.py runserver
```

---

## Training Data Requirements

### Minimum Data

- **Crop Recommendation**: At least 10-20 samples per crop (120-240 total)
- **Yield Prediction**: At least 10-20 samples per crop with yield data

### Recommended Data

- **Crop Recommendation**: 50+ samples per crop (600+ total)
- **Yield Prediction**: 50+ samples per crop with yield data

### Data Quality

- Complete soil data (pH, N, P, K, moisture)
- Weather data (temperature, rainfall, humidity)
- Location data (latitude, longitude)
- Accurate crop labels and yields

---

## Model Training Parameters

### Crop Recommendation Model

**Default Parameters:**
- `n_estimators`: 100 (number of trees)
- `max_depth`: None (unlimited depth)
- `class_weight`: 'balanced' (handles class imbalance)

**Customization:**
```python
# In train_crop_recommendation.py or via command line
trainer.train(
    X_train, y_train, X_val, y_val,
    n_estimators=200,  # More trees = better but slower
    max_depth=10       # Limit depth to prevent overfitting
)
```

### Yield Prediction Model

**Default Parameters:**
- `model_type`: 'random_forest'
- `n_estimators`: 100
- `max_depth`: None

**Model Types:**
- `random_forest`: Faster, good for most cases
- `gradient_boosting`: Slower but often more accurate

**Customization:**
```python
trainer.train(
    X_train, y_train, X_val, y_val,
    model_type='gradient_boosting',
    n_estimators=150,
    max_depth=8
)
```

---

## Troubleshooting

### Error: Preprocessed data not found

**Solution**: Run data preprocessing first
```bash
python ml_training/scripts/data_pipeline.py
```

### Error: Insufficient training data

**Solution**: Generate more synthetic data
```bash
python ml_training/scripts/generate_synthetic_data.py --synthetic-samples 100
```

### Low Model Performance

**Possible Causes:**
- Insufficient training data
- Poor data quality
- Feature mismatch

**Solutions:**
1. Collect more real data
2. Generate more synthetic data
3. Check data preprocessing
4. Try different hyperparameters

### Models Not Loading in Django

**Check:**
1. Models exist in `ml_training/models/`
2. File permissions are correct
3. Required packages installed (scikit-learn, numpy)
4. Check Django logs for errors

---

## Retraining Models

To retrain models with new data:

```bash
# 1. Collect new data (or generate more synthetic)
python ml_training/scripts/data_pipeline.py

# 2. Retrain models
python ml_training/scripts/train_models.py

# 3. Restart Django to load new models
python manage.py runserver
```

**Note**: Old models are overwritten. Backup if needed:
```bash
cp -r ml_training/models ml_training/models_backup
```

---

## Model Evaluation

After training, models are evaluated on a held-out test set:

### Crop Recommendation Metrics

- **Accuracy**: Overall correctness
- **Precision**: Weighted average precision
- **Recall**: Weighted average recall
- **F1 Score**: Weighted average F1
- **Per-Class Metrics**: Precision, recall, F1 for each crop
- **Confusion Matrix**: Shows prediction errors

### Yield Prediction Metrics

- **RMSE**: Root Mean Squared Error (in kg/ha)
- **MAE**: Mean Absolute Error (in kg/ha)
- **R² Score**: Coefficient of determination (0-1)
- **MAPE**: Mean Absolute Percentage Error (%)

---

## Next Steps After Training

1. **Verify Models Work**: Test recommendations in Django
2. **Monitor Performance**: Track prediction accuracy
3. **Collect Feedback**: Get user feedback on recommendations
4. **Improve Models**: Retrain with more data or better features
5. **Deploy**: Models are ready for production use

---

## Quick Start (Complete Example)

```bash
# Complete training workflow
cd /Users/vikasreddy/CropRecommendation
source venv/bin/activate

# Step 1: Generate and preprocess data
python ml_training/scripts/data_pipeline.py

# Step 2: Train models
python ml_training/scripts/train_models.py

# Step 3: Verify
ls -lh ml_training/models/*.pkl

# Step 4: Check metrics
python -c "import json; print(json.dumps(json.load(open('ml_training/models/crop_recommendation_metrics.json')), indent=2))"

# Step 5: Test in Django
python manage.py runserver
# Then request recommendations - they should use ML models!
```

---

## Summary

**Training Process:**
1. ✅ Prepare data (collect/generate + preprocess)
2. ✅ Train models (crop recommendation + yield prediction)
3. ✅ Evaluate models (check metrics)
4. ✅ Models automatically used by Django

**Time Required:**
- Data preprocessing: 1-2 minutes
- Model training: 2-5 minutes
- Total: ~5-10 minutes

**Output:**
- Trained models in `ml_training/models/`
- Evaluation metrics in JSON files
- Models automatically integrated with Django

The models are now ready to provide ML-powered crop recommendations and yield predictions! 🎉

