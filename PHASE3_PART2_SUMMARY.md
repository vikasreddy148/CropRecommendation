# Phase 3 Part 2: Crop Recommendation Model Training - COMPLETE ✅

## Summary

Phase 3 Part 2 has been successfully implemented. The ML model training pipeline is now ready to train both crop recommendation (classification) and yield prediction (regression) models. The system includes comprehensive training, evaluation, and model saving functionality.

---

## Features Implemented

### 1. Crop Recommendation Model Training ✅
- **File**: `ml_training/scripts/train_crop_recommendation.py`
- **Class**: `CropRecommendationTrainer`
- **Model Type**: Random Forest Classifier
- **Features**:
  - Multi-class classification (12 crops)
  - Handles class imbalance with balanced weights
  - Comprehensive evaluation metrics
  - Model saving with metadata
  - Prediction utilities

### 2. Yield Prediction Model Training ✅
- **File**: `ml_training/scripts/train_yield_prediction.py`
- **Class**: `YieldPredictionTrainer`
- **Model Types**: Random Forest Regressor, Gradient Boosting Regressor
- **Features**:
  - Regression model for yield prediction
  - Multiple regression metrics (RMSE, MAE, R², MAPE)
  - Model saving with metadata
  - Prediction utilities

### 3. Main Training Pipeline ✅
- **File**: `ml_training/scripts/train_models.py`
- **Function**: Orchestrates both model trainings
- **Features**:
  - Checks for preprocessed data
  - Trains both models sequentially
  - Error handling
  - Command-line interface
  - Training summary

### 4. Model Loading Utilities ✅
- **File**: `ml_training/scripts/load_models.py`
- **Class**: `ModelLoader`
- **Features**:
  - Load trained models
  - Load scalers and encoders
  - Prediction functions
  - Easy integration with Django

---

## Model Details

### Crop Recommendation Model

**Type**: Multi-class Classification  
**Algorithm**: Random Forest Classifier  
**Input Features**: 15-18 features (soil, weather, location, engineered features)  
**Output**: Crop name (12 classes)  
**Metrics**:
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1 Score (weighted)
- Per-class metrics
- Confusion matrix

**Classes** (12 crops):
- Rice, Wheat, Maize, Cotton, Sugarcane
- Potato, Tomato, Onion, Chilli
- Groundnut, Soybean, Pigeon Pea

### Yield Prediction Model

**Type**: Regression  
**Algorithm**: Random Forest Regressor / Gradient Boosting Regressor  
**Input Features**: 16-19 features (crop type, soil, weather, location, engineered features)  
**Output**: Yield in kg/hectare (continuous)  
**Metrics**:
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- R² Score (Coefficient of Determination)
- MAPE (Mean Absolute Percentage Error)

---

## File Structure

```
ml_training/
├── models/                          # Trained models (created after training)
│   ├── crop_recommendation_model.pkl
│   ├── crop_recommendation_scaler.pkl
│   ├── crop_recommendation_encoder.pkl
│   ├── crop_recommendation_model_metadata.json
│   ├── crop_recommendation_metrics.json
│   ├── yield_prediction_model.pkl
│   ├── yield_prediction_scaler.pkl
│   ├── yield_prediction_y_scaler.pkl
│   ├── yield_prediction_encoder.pkl
│   ├── yield_prediction_model_metadata.json
│   └── yield_prediction_metrics.json
└── scripts/
    ├── train_crop_recommendation.py  # Crop recommendation trainer
    ├── train_yield_prediction.py     # Yield prediction trainer
    ├── train_models.py               # Main training pipeline
    └── load_models.py                # Model loading utilities
```

---

## Usage

### Train Both Models

```bash
# From project root
python ml_training/scripts/train_models.py
```

### Train Individual Models

```bash
# Train only crop recommendation model
python ml_training/scripts/train_crop_recommendation.py

# Train only yield prediction model
python ml_training/scripts/train_yield_prediction.py
```

### Command-Line Options

```bash
# Train with custom parameters
python ml_training/scripts/train_models.py \
    --n-estimators 200 \
    --max-depth 10

# Train only crop recommendation
python ml_training/scripts/train_models.py --crop-only

# Train only yield prediction with gradient boosting
python ml_training/scripts/train_models.py \
    --yield-only \
    --model-type gradient_boosting
```

### Load Models for Inference

```python
from ml_training.scripts.load_models import ModelLoader

loader = ModelLoader()

# Load crop recommendation model
crop_model = loader.load_crop_recommendation_model()

# Load yield prediction model
yield_model = loader.load_yield_prediction_model()

# Make predictions
crop_name, confidence, all_probs = loader.predict_crop(features)
yield_pred = loader.predict_yield(features)
```

---

## Training Process

### 1. Data Loading
- Loads preprocessed data from `ml_training/data/`
- Loads scalers and encoders
- Loads metadata

### 2. Model Training
- **Crop Recommendation**: Random Forest with balanced class weights
- **Yield Prediction**: Random Forest or Gradient Boosting
- Validates on validation set during training

### 3. Evaluation
- Evaluates on test set
- Calculates comprehensive metrics
- Prints detailed results

### 4. Model Saving
- Saves trained model (`.pkl`)
- Saves scalers and encoders
- Saves metadata (JSON)
- Saves evaluation metrics (JSON)

---

## Evaluation Metrics

### Crop Recommendation (Classification)

**Overall Metrics**:
- **Accuracy**: Overall correctness
- **Precision**: Weighted average precision
- **Recall**: Weighted average recall
- **F1 Score**: Weighted average F1

**Per-Class Metrics**:
- Precision per crop
- Recall per crop
- F1 score per crop
- Support (number of samples)

**Visualization**:
- Confusion matrix
- Classification report

### Yield Prediction (Regression)

**Metrics**:
- **RMSE**: Root Mean Squared Error (in kg/ha)
- **MAE**: Mean Absolute Error (in kg/ha)
- **R² Score**: Coefficient of determination (0-1, higher is better)
- **MAPE**: Mean Absolute Percentage Error (%)

**Interpretation**:
- Lower RMSE/MAE = Better predictions
- Higher R² = Better fit (1.0 = perfect)
- Lower MAPE = Better accuracy

---

## Model Performance

### Expected Performance

**Crop Recommendation**:
- Accuracy: 70-90% (depending on data quality)
- F1 Score: 0.70-0.90
- Good performance on common crops
- May struggle with similar crops

**Yield Prediction**:
- RMSE: 10-20% of average yield
- R²: 0.60-0.85
- Better for crops with more training data
- Accuracy improves with more features

### Improving Performance

1. **More Training Data**: Collect more real-world data
2. **Feature Engineering**: Add more relevant features
3. **Hyperparameter Tuning**: Optimize model parameters
4. **Ensemble Methods**: Combine multiple models
5. **Deep Learning**: Use neural networks for complex patterns

---

## Integration with Django

### Using Models in Django

```python
from ml_training.scripts.load_models import ModelLoader
from ml_training.scripts.preprocess_data import DataPreprocessor

# Load models
loader = ModelLoader()

# Prepare features from field data
# (Use same feature engineering as training)

# Predict crop
crop_name, confidence, probabilities = loader.predict_crop(features)

# Predict yield
yield_pred = loader.predict_yield(features)
```

### Updating Recommendation Service

The trained models can be integrated into `apps/recommendations/services.py` to replace or enhance the rule-based logic.

---

## Requirements

### Python Packages

All required packages are in `requirements.txt`:
- scikit-learn (for Random Forest, Gradient Boosting)
- numpy (for array operations)
- pandas (for data handling)

### Preprocessed Data

Before training, ensure you have:
- Preprocessed data files in `ml_training/data/`
- Train/val/test splits
- Scalers and encoders

Run data preprocessing first:
```bash
python ml_training/scripts/data_pipeline.py
```

---

## Troubleshooting

### Error: Preprocessed data not found

**Solution**: Run data preprocessing first
```bash
python ml_training/scripts/data_pipeline.py
```

### Error: Model training fails

**Possible causes**:
- Insufficient training data
- Missing features
- Data format mismatch

**Solution**: Check data files and ensure they match expected format

### Low Model Performance

**Possible causes**:
- Insufficient training data
- Poor feature quality
- Class imbalance

**Solutions**:
- Generate more synthetic data
- Improve feature engineering
- Use class weights (already implemented)
- Try different algorithms

---

## Next Steps

After completing Phase 3 Part 2:

1. **Review Model Performance** ✅
   - Check evaluation metrics
   - Analyze confusion matrix
   - Identify areas for improvement

2. **Phase 3 Part 3: Model Integration** ⏭️
   - Integrate models with Django
   - Update recommendation service
   - Add ML-based predictions to UI
   - Test end-to-end workflow

3. **Model Optimization** (Optional)
   - Hyperparameter tuning
   - Feature selection
   - Model ensemble
   - Cross-validation

---

## Files Created

1. `ml_training/scripts/train_crop_recommendation.py` - Crop recommendation trainer
2. `ml_training/scripts/train_yield_prediction.py` - Yield prediction trainer
3. `ml_training/scripts/train_models.py` - Main training pipeline
4. `ml_training/scripts/load_models.py` - Model loading utilities
5. `PHASE3_PART2_SUMMARY.md` - This file

---

## Status: ✅ COMPLETE

Phase 3 Part 2 is complete with:
- ✅ Crop recommendation model training (classification)
- ✅ Yield prediction model training (regression)
- ✅ Comprehensive evaluation metrics
- ✅ Model saving and loading utilities
- ✅ Main training pipeline
- ✅ Documentation

The system is ready for Phase 3 Part 3: Model Integration!

---

## Usage Example

```bash
# Step 1: Preprocess data (if not done)
python ml_training/scripts/data_pipeline.py

# Step 2: Train models
python ml_training/scripts/train_models.py

# Step 3: Check results
ls ml_training/models/
cat ml_training/models/crop_recommendation_metrics.json
cat ml_training/models/yield_prediction_metrics.json
```

---

**Phase 3 Part 2: Crop Recommendation Model Training - COMPLETE! ✅**

Ready to proceed with Phase 3 Part 3: Model Integration.

