"""
Recommendation service for crop recommendations.
Uses ML models when available, falls back to rule-based logic.
Enhanced with sophisticated business logic for Phase 4.
"""
import logging
from typing import Dict, List, Optional
from decimal import Decimal
from django.utils import timezone
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Try to import ML service
try:
    from .ml_service import get_ml_service
    ML_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    ML_AVAILABLE = False
    logger.debug(f"ML service not available: {e}. Using rule-based recommendations only.")

# Import enhanced business logic
try:
    from .business_logic import (
        CropRotationAnalyzer,
        ProfitCalculator,
        SustainabilityScorer,
        RecommendationRanker,
        ExplainabilityGenerator
    )
    BUSINESS_LOGIC_AVAILABLE = True
except ImportError as e:
    BUSINESS_LOGIC_AVAILABLE = False
    logger.warning(f"Enhanced business logic not available: {e}. Using basic logic.")


class CropRecommendationService:
    """Service for generating crop recommendations based on soil and weather data."""
    
    # Crop requirements database
    # Format: crop_name: {requirements}
    CROP_REQUIREMENTS = {
        'Rice': {
            'ph_min': 5.0,
            'ph_max': 7.5,
            'n_min': 100,
            'p_min': 20,
            'k_min': 40,
            'moisture_min': 60,
            'temperature_min': 20,
            'temperature_max': 35,
            'rainfall_min': 1000,
            'season': ['kharif'],
            'sustainability_score': 75,
        },
        'Wheat': {
            'ph_min': 6.0,
            'ph_max': 7.5,
            'n_min': 120,
            'p_min': 30,
            'k_min': 50,
            'moisture_min': 40,
            'temperature_min': 15,
            'temperature_max': 25,
            'rainfall_min': 500,
            'season': ['rabi'],
            'sustainability_score': 80,
        },
        'Maize': {
            'ph_min': 5.5,
            'ph_max': 7.0,
            'n_min': 150,
            'p_min': 25,
            'k_min': 60,
            'moisture_min': 50,
            'temperature_min': 18,
            'temperature_max': 30,
            'rainfall_min': 600,
            'season': ['kharif', 'zaid'],
            'sustainability_score': 70,
        },
        'Cotton': {
            'ph_min': 5.5,
            'ph_max': 8.0,
            'n_min': 80,
            'p_min': 20,
            'k_min': 50,
            'moisture_min': 50,
            'temperature_min': 21,
            'temperature_max': 35,
            'rainfall_min': 500,
            'season': ['kharif'],
            'sustainability_score': 65,
        },
        'Sugarcane': {
            'ph_min': 6.0,
            'ph_max': 7.5,
            'n_min': 200,
            'p_min': 40,
            'k_min': 100,
            'moisture_min': 70,
            'temperature_min': 20,
            'temperature_max': 35,
            'rainfall_min': 1200,
            'season': ['year_round'],
            'sustainability_score': 60,
        },
        'Potato': {
            'ph_min': 4.8,
            'ph_max': 5.5,
            'n_min': 100,
            'p_min': 50,
            'k_min': 150,
            'moisture_min': 60,
            'temperature_min': 15,
            'temperature_max': 25,
            'rainfall_min': 500,
            'season': ['rabi', 'zaid'],
            'sustainability_score': 75,
        },
        'Tomato': {
            'ph_min': 6.0,
            'ph_max': 7.0,
            'n_min': 120,
            'p_min': 40,
            'k_min': 120,
            'moisture_min': 60,
            'temperature_min': 18,
            'temperature_max': 28,
            'rainfall_min': 400,
            'season': ['year_round'],
            'sustainability_score': 70,
        },
        'Onion': {
            'ph_min': 6.0,
            'ph_max': 7.0,
            'n_min': 100,
            'p_min': 30,
            'k_min': 80,
            'moisture_min': 50,
            'temperature_min': 13,
            'temperature_max': 25,
            'rainfall_min': 400,
            'season': ['rabi', 'kharif'],
            'sustainability_score': 75,
        },
        'Chilli': {
            'ph_min': 6.0,
            'ph_max': 7.0,
            'n_min': 100,
            'p_min': 30,
            'k_min': 100,
            'moisture_min': 50,
            'temperature_min': 20,
            'temperature_max': 30,
            'rainfall_min': 400,
            'season': ['kharif', 'rabi'],
            'sustainability_score': 70,
        },
        'Groundnut': {
            'ph_min': 6.0,
            'ph_max': 7.5,
            'n_min': 20,
            'p_min': 20,
            'k_min': 40,
            'moisture_min': 40,
            'temperature_min': 20,
            'temperature_max': 35,
            'rainfall_min': 500,
            'season': ['kharif', 'rabi'],
            'sustainability_score': 80,
        },
        'Soybean': {
            'ph_min': 6.0,
            'ph_max': 7.0,
            'n_min': 20,
            'p_min': 30,
            'k_min': 50,
            'moisture_min': 50,
            'temperature_min': 20,
            'temperature_max': 30,
            'rainfall_min': 600,
            'season': ['kharif'],
            'sustainability_score': 85,
        },
        'Pigeon Pea': {
            'ph_min': 6.0,
            'ph_max': 7.5,
            'n_min': 20,
            'p_min': 20,
            'k_min': 30,
            'moisture_min': 40,
            'temperature_min': 20,
            'temperature_max': 35,
            'rainfall_min': 600,
            'season': ['kharif'],
            'sustainability_score': 90,
        },
        'Chickpea': {
            'ph_min': 6.0,
            'ph_max': 8.5,
            'n_min': 40,
            'p_min': 60,
            'k_min': 80,
            'moisture_min': 30,
            'temperature_min': 17,
            'temperature_max': 21,
            'rainfall_min': 60,
            'season': ['rabi'],
            'sustainability_score': 85,
        },
        'Kidneybeans': {
            'ph_min': 5.5,
            'ph_max': 6.0,
            'n_min': 20,
            'p_min': 60,
            'k_min': 20,
            'moisture_min': 40,
            'temperature_min': 15,
            'temperature_max': 25,
            'rainfall_min': 60,
            'season': ['kharif', 'rabi'],
            'sustainability_score': 80,
        },
        'Mothbeans': {
            'ph_min': 6.5,
            'ph_max': 8.5,
            'n_min': 20,
            'p_min': 40,
            'k_min': 20,
            'moisture_min': 30,
            'temperature_min': 24,
            'temperature_max': 30,
            'rainfall_min': 30,
            'season': ['kharif'],
            'sustainability_score': 85,
        },
        'Mungbean': {
            'ph_min': 6.0,
            'ph_max': 7.0,
            'n_min': 20,
            'p_min': 40,
            'k_min': 20,
            'moisture_min': 40,
            'temperature_min': 27,
            'temperature_max': 29,
            'rainfall_min': 35,
            'season': ['kharif', 'zaid'],
            'sustainability_score': 85,
        },
        'Blackgram': {
            'ph_min': 6.5,
            'ph_max': 7.5,
            'n_min': 40,
            'p_min': 60,
            'k_min': 20,
            'moisture_min': 40,
            'temperature_min': 25,
            'temperature_max': 35,
            'rainfall_min': 60,
            'season': ['kharif', 'rabi'],
            'sustainability_score': 80,
        },
        'Lentil': {
            'ph_min': 6.0,
            'ph_max': 7.0,
            'n_min': 20,
            'p_min': 60,
            'k_min': 20,
            'moisture_min': 30,
            'temperature_min': 18,
            'temperature_max': 30,
            'rainfall_min': 35,
            'season': ['rabi'],
            'sustainability_score': 85,
        },
        'Pomegranate': {
            'ph_min': 5.5,
            'ph_max': 7.5,
            'n_min': 20,
            'p_min': 10,
            'k_min': 40,
            'moisture_min': 40,
            'temperature_min': 18,
            'temperature_max': 25,
            'rainfall_min': 100,
            'season': ['year_round'],
            'sustainability_score': 75,
        },
        'Banana': {
            'ph_min': 5.5,
            'ph_max': 6.5,
            'n_min': 100,
            'p_min': 80,
            'k_min': 50,
            'moisture_min': 70,
            'temperature_min': 25,
            'temperature_max': 30,
            'rainfall_min': 90,
            'season': ['year_round'],
            'sustainability_score': 65,
        },
        'Mango': {
            'ph_min': 4.5,
            'ph_max': 7.0,
            'n_min': 20,
            'p_min': 20,
            'k_min': 30,
            'moisture_min': 50,
            'temperature_min': 27,
            'temperature_max': 35,
            'rainfall_min': 90,
            'season': ['year_round'],
            'sustainability_score': 70,
        },
        'Grapes': {
            'ph_min': 5.5,
            'ph_max': 7.0,
            'n_min': 20,
            'p_min': 130,
            'k_min': 200,
            'moisture_min': 50,
            'temperature_min': 20,
            'temperature_max': 40,
            'rainfall_min': 65,
            'season': ['year_round'],
            'sustainability_score': 75,
        },
        'Watermelon': {
            'ph_min': 6.0,
            'ph_max': 7.0,
            'n_min': 40,
            'p_min': 20,
            'k_min': 50,
            'moisture_min': 60,
            'temperature_min': 24,
            'temperature_max': 27,
            'rainfall_min': 40,
            'season': ['zaid', 'kharif'],
            'sustainability_score': 70,
        },
        'Muskmelon': {
            'ph_min': 6.0,
            'ph_max': 6.5,
            'n_min': 100,
            'p_min': 20,
            'k_min': 50,
            'moisture_min': 50,
            'temperature_min': 28,
            'temperature_max': 35,
            'rainfall_min': 20,
            'season': ['zaid'],
            'sustainability_score': 70,
        },
        'Apple': {
            'ph_min': 5.5,
            'ph_max': 6.5,
            'n_min': 20,
            'p_min': 130,
            'k_min': 200,
            'moisture_min': 60,
            'temperature_min': 21,
            'temperature_max': 24,
            'rainfall_min': 100,
            'season': ['year_round'],
            'sustainability_score': 65,
        },
        'Orange': {
            'ph_min': 6.0,
            'ph_max': 8.0,
            'n_min': 20,
            'p_min': 10,
            'k_min': 10,
            'moisture_min': 50,
            'temperature_min': 10,
            'temperature_max': 35,
            'rainfall_min': 100,
            'season': ['year_round'],
            'sustainability_score': 70,
        },
        'Papaya': {
            'ph_min': 5.5,
            'ph_max': 7.0,
            'n_min': 40,
            'p_min': 50,
            'k_min': 50,
            'moisture_min': 60,
            'temperature_min': 23,
            'temperature_max': 45,
            'rainfall_min': 150,
            'season': ['year_round'],
            'sustainability_score': 60,
        },
        'Coconut': {
            'ph_min': 5.0,
            'ph_max': 6.5,
            'n_min': 20,
            'p_min': 20,
            'k_min': 30,
            'moisture_min': 80,
            'temperature_min': 25,
            'temperature_max': 30,
            'rainfall_min': 150,
            'season': ['year_round'],
            'sustainability_score': 80,
        },
        'Jute': {
            'ph_min': 6.0,
            'ph_max': 7.0,
            'n_min': 80,
            'p_min': 40,
            'k_min': 40,
            'moisture_min': 70,
            'temperature_min': 23,
            'temperature_max': 25,
            'rainfall_min': 150,
            'season': ['kharif'],
            'sustainability_score': 70,
        },
        'Coffee': {
            'ph_min': 6.0,
            'ph_max': 6.5,
            'n_min': 100,
            'p_min': 30,
            'k_min': 30,
            'moisture_min': 60,
            'temperature_min': 23,
            'temperature_max': 28,
            'rainfall_min': 140,
            'season': ['year_round'],
            'sustainability_score': 65,
        },
    }
    
    # Average yield in kg/hectare (can be improved with ML)
    AVERAGE_YIELDS = {
        'Rice': 3000,
        'Wheat': 3500,
        'Maize': 4000,
        'Cotton': 500,
        'Sugarcane': 70000,
        'Potato': 25000,
        'Tomato': 30000,
        'Onion': 20000,
        'Chilli': 15000,
        'Groundnut': 2000,
        'Soybean': 2500,
        'Pigeon Pea': 1200,
        'Chickpea': 1500,
        'Kidneybeans': 1200,
        'Mothbeans': 800,
        'Mungbean': 1000,
        'Blackgram': 1100,
        'Lentil': 900,
        'Pomegranate': 12000,
        'Banana': 35000,
        'Mango': 10000,
        'Grapes': 20000,
        'Watermelon': 25000,
        'Muskmelon': 18000,
        'Apple': 15000,
        'Orange': 20000,
        'Papaya': 40000,
        'Coconut': 10000,
        'Jute': 2500,
        'Coffee': 800,
    }
    
    # Average profit per hectare (in local currency - approximate)
    AVERAGE_PROFITS = {
        'Rice': 50000,
        'Wheat': 60000,
        'Maize': 55000,
        'Cotton': 80000,
        'Sugarcane': 150000,
        'Potato': 200000,
        'Tomato': 250000,
        'Onion': 180000,
        'Chilli': 200000,
        'Groundnut': 70000,
        'Soybean': 60000,
        'Pigeon Pea': 50000,
        'Chickpea': 75000,
        'Kidneybeans': 70000,
        'Mothbeans': 40000,
        'Mungbean': 50000,
        'Blackgram': 55000,
        'Lentil': 45000,
        'Pomegranate': 300000,
        'Banana': 250000,
        'Mango': 400000,
        'Grapes': 500000,
        'Watermelon': 150000,
        'Muskmelon': 130000,
        'Apple': 450000,
        'Orange': 350000,
        'Papaya': 400000,
        'Coconut': 200000,
        'Jute': 60000,
        'Coffee': 120000,
    }
    
    @classmethod
    def get_current_season(cls) -> str:
        """Determine current season based on date."""
        month = timezone.now().month
        if month in [6, 7, 8, 9, 10]:  # June to October
            return 'kharif'
        elif month in [11, 12, 1, 2, 3]:  # November to March
            return 'rabi'
        else:  # April, May
            return 'zaid'
    
    @classmethod
    def calculate_compatibility_score(
        cls,
        crop: str,
        soil_ph: Optional[float],
        soil_n: Optional[float],
        soil_p: Optional[float],
        soil_k: Optional[float],
        soil_moisture: Optional[float],
        temperature: Optional[float],
        rainfall: Optional[float],
        season: Optional[str] = None
    ) -> Dict:
        """
        Calculate compatibility score for a crop based on conditions.
        
        Returns:
            Dictionary with score, reasons, and match details
        """
        if crop not in cls.CROP_REQUIREMENTS:
            return {
                'score': 0,
                'reasons': ['Crop not in database'],
                'match_details': {}
            }
        
        requirements = cls.CROP_REQUIREMENTS[crop]
        score = 100
        reasons = []
        match_details = {}
        
        # Check pH
        if soil_ph is not None:
            ph_min = requirements['ph_min']
            ph_max = requirements['ph_max']
            if ph_min <= soil_ph <= ph_max:
                match_details['ph'] = 'optimal'
            elif abs(soil_ph - ph_min) < 0.5 or abs(soil_ph - ph_max) < 0.5:
                score -= 10
                match_details['ph'] = 'acceptable'
                reasons.append(f'pH ({soil_ph}) slightly outside optimal range ({ph_min}-{ph_max})')
            elif abs(soil_ph - ph_min) > 1.5 or abs(soil_ph - ph_max) > 1.5:
                score -= 40
                match_details['ph'] = 'severe_mismatch'
                reasons.append(f'Severe pH deviation ({soil_ph}) from optimal ({ph_min}-{ph_max})')
            else:
                score -= 30
                match_details['ph'] = 'poor'
                reasons.append(f'pH ({soil_ph}) outside optimal range ({ph_min}-{ph_max})')
        else:
            score -= 5
            match_details['ph'] = 'unknown'
        
        # Check nutrients
        if soil_n is not None:
            n_min = requirements['n_min']
            if soil_n >= n_min:
                match_details['n'] = 'sufficient'
            elif soil_n >= n_min * 0.7:
                score -= 5
                match_details['n'] = 'low'
                reasons.append(f'Nitrogen ({soil_n} kg/ha) below optimal ({n_min} kg/ha)')
            else:
                score -= 15
                match_details['n'] = 'deficient'
                reasons.append(f'Nitrogen ({soil_n} kg/ha) significantly below optimal ({n_min} kg/ha)')
        else:
            score -= 3
            match_details['n'] = 'unknown'
        
        if soil_p is not None:
            p_min = requirements['p_min']
            if soil_p >= p_min:
                match_details['p'] = 'sufficient'
            elif soil_p >= p_min * 0.7:
                score -= 5
                match_details['p'] = 'low'
                reasons.append(f'Phosphorus ({soil_p} kg/ha) below optimal ({p_min} kg/ha)')
            else:
                score -= 15
                match_details['p'] = 'deficient'
                reasons.append(f'Phosphorus ({soil_p} kg/ha) significantly below optimal ({p_min} kg/ha)')
        else:
            score -= 3
            match_details['p'] = 'unknown'
        
        if soil_k is not None:
            k_min = requirements['k_min']
            if soil_k >= k_min:
                match_details['k'] = 'sufficient'
            elif soil_k >= k_min * 0.7:
                score -= 5
                match_details['k'] = 'low'
                reasons.append(f'Potassium ({soil_k} kg/ha) below optimal ({k_min} kg/ha)')
            else:
                score -= 15
                match_details['k'] = 'deficient'
                reasons.append(f'Potassium ({soil_k} kg/ha) significantly below optimal ({k_min} kg/ha)')
        else:
            score -= 3
            match_details['k'] = 'unknown'

        # Check nutrient imbalance (N vs P)
        if soil_n is not None and soil_p is not None and soil_p > 0 and soil_n > 0:
            if (soil_n / soil_p) > 5.0 or (soil_p / soil_n) > 5.0:
                score -= 10
                reasons.append('Nutrient imbalance detected between Nitrogen and Phosphorus')
        
        # Check moisture
        if soil_moisture is not None:
            moisture_min = requirements['moisture_min']
            if soil_moisture >= moisture_min:
                match_details['moisture'] = 'sufficient'
            elif soil_moisture >= moisture_min * 0.8:
                score -= 5
                match_details['moisture'] = 'low'
                reasons.append(f'Moisture ({soil_moisture}%) below optimal ({moisture_min}%)')
            else:
                score -= 15
                match_details['moisture'] = 'deficient'
                reasons.append(f'Moisture ({soil_moisture}%) significantly below optimal ({moisture_min}%)')
        else:
            score -= 3
            match_details['moisture'] = 'unknown'
        
        # Check temperature
        if temperature is not None:
            temp_min = requirements['temperature_min']
            temp_max = requirements['temperature_max']
            if temp_min <= temperature <= temp_max:
                match_details['temperature'] = 'optimal'
            elif abs(temperature - temp_min) < 3 or abs(temperature - temp_max) < 3:
                score -= 5
                match_details['temperature'] = 'acceptable'
                reasons.append(f'Temperature ({temperature}°C) slightly outside optimal range ({temp_min}-{temp_max}°C)')
            elif abs(temperature - temp_min) > 6 or abs(temperature - temp_max) > 6:
                score -= 25
                match_details['temperature'] = 'severe_stress'
                reasons.append(f'Severe temperature stress ({temperature}°C) outside optimal ({temp_min}-{temp_max}°C)')
            else:
                score -= 15
                match_details['temperature'] = 'poor'
                reasons.append(f'Temperature ({temperature}°C) outside optimal range ({temp_min}-{temp_max}°C)')
        else:
            score -= 3
            match_details['temperature'] = 'unknown'
        
        # Check season
        if season is None:
            season = cls.get_current_season()
        
        if season in requirements['season'] or 'year_round' in requirements['season']:
            match_details['season'] = 'suitable'
        else:
            score -= 20
            match_details['season'] = 'unsuitable'
            reasons.append(f'Current season ({season}) not ideal for {crop}')
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        # Apply hard threshold penalties/tags
        if score < 20:
            reasons.append('CRITICAL: Extremely low compatibility (<20%) - severe agronomic mismatch.')
        if score < 10:
            reasons.append('CRITICAL: Recommendation confidence is very low (<10%).')
        if score < 5:
            reasons.append('CRITICAL: Crop is fundamentally unsuitable (<5%) and should be suppressed.')
        
        if score >= 80:
            reasons.insert(0, 'Excellent match for current conditions')
        elif score >= 60:
            reasons.insert(0, 'Good match for current conditions')
        elif score >= 40:
            reasons.insert(0, 'Moderate match - some conditions need improvement')
        else:
            reasons.insert(0, 'Poor match - significant improvements needed')
        
        return {
            'score': round(score, 2),
            'reasons': reasons,
            'match_details': match_details
        }
    
    @classmethod
    def get_recommendations(
        cls,
        soil_ph: Optional[float] = None,
        soil_n: Optional[float] = None,
        soil_p: Optional[float] = None,
        soil_k: Optional[float] = None,
        soil_moisture: Optional[float] = None,
        temperature: Optional[float] = None,
        rainfall: Optional[float] = None,
        humidity: Optional[float] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        season: Optional[str] = None,
        limit: int = 3,
        use_ml: bool = True
    ) -> List[Dict]:
        """
        Get crop recommendations based on soil and weather conditions.
        Uses ML models if available, otherwise falls back to rule-based logic.
        """
        # Try ML models first if available and requested
        if use_ml and ML_AVAILABLE:
            try:
                ml_service = get_ml_service()
                ml_recommendations = ml_service.predict_crop_recommendations(
                    soil_ph=soil_ph,
                    soil_n=soil_n,
                    soil_p=soil_p,
                    soil_k=soil_k,
                    soil_moisture=soil_moisture,
                    temperature=temperature,
                    rainfall=rainfall,
                    humidity=humidity,
                    latitude=latitude,
                    longitude=longitude,
                    season=season,
                    limit=limit * 2  # Fetch more to allow proper filtering
                )
                
                if ml_recommendations:
                    enhanced_recommendations = []
                    for rec in ml_recommendations:
                        crop_name = rec['crop_name']
                        ml_probability = rec['confidence_score']
                        
                        # Compute true agronomic compatibility score
                        compatibility = cls.calculate_compatibility_score(
                            crop=crop_name,
                            soil_ph=soil_ph,
                            soil_n=soil_n,
                            soil_p=soil_p,
                            soil_k=soil_k,
                            soil_moisture=soil_moisture,
                            temperature=temperature,
                            rainfall=rainfall,
                            season=season
                        )
                        compat_score = compatibility['score']
                        
                        # Get yield prediction from ML model
                        ml_yield = ml_service.predict_yield(
                            crop_name=crop_name,
                            soil_ph=soil_ph,
                            soil_n=soil_n,
                            soil_p=soil_p,
                            soil_k=soil_k,
                            soil_moisture=soil_moisture,
                            temperature=temperature,
                            rainfall=rainfall,
                            humidity=humidity,
                            latitude=latitude,
                            longitude=longitude,
                            season=season
                        )
                        
                        if ml_yield is not None:
                            raw_yield = ml_yield
                        else:
                            raw_yield = cls.AVERAGE_YIELDS.get(crop_name, 1000)
                            
                        # REQUIRED HYBRID YIELD FORMULA: Final Yield = ML_Yield × (0.4 + 0.6 × Compatibility/100)
                        final_yield = raw_yield * (0.4 + 0.6 * (compat_score / 100.0))
                        
                        # Clamp upper bound per crop
                        max_possible_yield = cls.AVERAGE_YIELDS.get(crop_name, 1000) * 2.5
                        final_yield = max(0.0, min(final_yield, max_possible_yield))
                        
                        # Use enhanced profit calculator
                        if BUSINESS_LOGIC_AVAILABLE:
                            profit_data = ProfitCalculator.calculate_profit(
                                crop_name=crop_name,
                                expected_yield=final_yield,
                                yield_multiplier=1.0,
                                risk_adjustment=1.0,
                                compatibility_score=compat_score
                            )
                            profit_margin = profit_data['risk_adjusted_profit']
                            profit_details = profit_data
                        else:
                            profit_per_kg = cls.AVERAGE_PROFITS.get(crop_name, 0) / max(cls.AVERAGE_YIELDS.get(crop_name, 1), 1)
                            profit_margin = final_yield * profit_per_kg
                            profit_details = {'profit_margin': profit_margin}
                        
                        # Use enhanced sustainability scorer
                        if BUSINESS_LOGIC_AVAILABLE:
                            sustainability_data = SustainabilityScorer.calculate_sustainability_score(
                                crop_name=crop_name,
                                water_availability=rainfall * 1000 if rainfall else None,
                                soil_health_bonus=0.0,
                                rotation_bonus=0.0
                            )
                            sustainability_score = sustainability_data['sustainability_score']
                            sustainability_details = sustainability_data
                        else:
                            sustainability_score = cls.CROP_REQUIREMENTS.get(crop_name, {}).get('sustainability_score', 70)
                            sustainability_details = {}
                            
                        # Generate Explainability insights
                        reasons = compatibility['reasons']
                        explanation = {}
                        if BUSINESS_LOGIC_AVAILABLE:
                            explanation = ExplainabilityGenerator.generate_explanation(
                                crop_name=crop_name,
                                compatibility_score=compat_score,
                                expected_yield=final_yield,
                                profit_margin=profit_margin,
                                roi=profit_details.get('roi', 0),
                                reasons=reasons
                            )
                        
                        enhanced_rec = {
                            'crop_name': crop_name,
                            'confidence_score': compat_score,
                            'ml_probability': ml_probability,
                            'expected_yield': round(final_yield, 2),
                            'profit_margin': round(profit_margin, 2),
                            'sustainability_score': sustainability_score,
                            'reasons': reasons,
                            'explanation': explanation,
                            'match_details': compatibility['match_details'],
                            'ml_prediction': True,
                            'profit_details': profit_details,
                            'sustainability_details': sustainability_details,
                        }
                        enhanced_recommendations.append(enhanced_rec)
                    
                    # Sort by agronomic compatibility score
                    enhanced_recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
                    logger.info(f"Using ML model for recommendations. Generated {len(enhanced_recommendations)} recommendations.")
                    return enhanced_recommendations[:limit]
                    
            except Exception as e:
                logger.warning(f"ML model prediction failed: {e}. Falling back to rule-based logic.")
        
        # Fallback to rule-based logic with enhanced business logic
        recommendations = []
        
        for crop in cls.CROP_REQUIREMENTS.keys():
            compatibility = cls.calculate_compatibility_score(
                crop=crop,
                soil_ph=soil_ph,
                soil_n=soil_n,
                soil_p=soil_p,
                soil_k=soil_k,
                soil_moisture=soil_moisture,
                temperature=temperature,
                rainfall=rainfall,
                season=season
            )
            compat_score = compatibility['score']
            
            raw_yield = cls.AVERAGE_YIELDS.get(crop, 1000)
            final_yield = raw_yield * (0.4 + 0.6 * (compat_score / 100.0))
            max_possible_yield = raw_yield * 2.5
            final_yield = max(0.0, min(final_yield, max_possible_yield))
            
            if BUSINESS_LOGIC_AVAILABLE:
                profit_data = ProfitCalculator.calculate_profit(
                    crop_name=crop,
                    expected_yield=final_yield,
                    yield_multiplier=1.0,
                    risk_adjustment=1.0,
                    compatibility_score=compat_score
                )
                profit_margin = profit_data['risk_adjusted_profit']
                profit_details = profit_data
            else:
                profit_margin = cls.AVERAGE_PROFITS.get(crop, 0) * (compat_score / 100.0)
                profit_details = {'profit_margin': profit_margin}
            
            if BUSINESS_LOGIC_AVAILABLE:
                sustainability_data = SustainabilityScorer.calculate_sustainability_score(
                    crop_name=crop,
                    water_availability=rainfall * 1000 if rainfall else None,
                    soil_health_bonus=0.0,
                    rotation_bonus=0.0
                )
                sustainability_score = sustainability_data['sustainability_score']
                sustainability_details = sustainability_data
            else:
                sustainability_score = cls.CROP_REQUIREMENTS[crop]['sustainability_score']
                sustainability_details = {}
                
            explanation = {}
            if BUSINESS_LOGIC_AVAILABLE:
                explanation = ExplainabilityGenerator.generate_explanation(
                    crop_name=crop,
                    compatibility_score=compat_score,
                    expected_yield=final_yield,
                    profit_margin=profit_margin,
                    roi=profit_details.get('roi', 0),
                    reasons=compatibility['reasons']
                )
            
            recommendation = {
                'crop_name': crop,
                'confidence_score': compat_score,
                'ml_probability': None,
                'expected_yield': round(final_yield, 2),
                'profit_margin': round(profit_margin, 2),
                'sustainability_score': sustainability_score,
                'reasons': compatibility['reasons'],
                'explanation': explanation,
                'match_details': compatibility['match_details'],
                'ml_prediction': False,
                'profit_details': profit_details,
                'sustainability_details': sustainability_details,
            }
            
            recommendations.append(recommendation)
        
        recommendations.sort(key=lambda x: x['confidence_score'], reverse=True)
        return recommendations[:limit]
    
    @classmethod
    def get_recommendation_for_field(
        cls,
        field,
        weather_data=None,
        limit: int = 3,
        use_ml: bool = True
    ) -> List[Dict]:
        """
        Get recommendations for a specific field with enhanced business logic.
        """
        # Get soil data from field
        soil_ph = float(field.soil_ph) if field.soil_ph else None
        soil_n = float(field.n_content) if field.n_content else None
        soil_p = float(field.p_content) if field.p_content else None
        soil_k = float(field.k_content) if field.k_content else None
        soil_moisture = float(field.soil_moisture) if field.soil_moisture else None
        
        # Get location
        latitude = None
        longitude = None
        if field.latitude and field.longitude:
            latitude = float(field.latitude)
            longitude = float(field.longitude)
        elif field.farm.latitude and field.farm.longitude:
            latitude = float(field.farm.latitude)
            longitude = float(field.farm.longitude)
        
        # Get weather data
        temperature = None
        rainfall = None
        humidity = None
        if weather_data:
            temperature = float(weather_data.temperature) if weather_data.temperature else None
            rainfall = float(weather_data.rainfall) if weather_data.rainfall else None
            humidity = float(weather_data.humidity) if weather_data.humidity else None
        
        # Get latest soil data if available
        latest_soil = field.soil_data.first() if hasattr(field, 'soil_data') else None
        if latest_soil:
            soil_ph = float(latest_soil.ph) if latest_soil.ph else soil_ph
            soil_n = float(latest_soil.n) if latest_soil.n else soil_n
            soil_p = float(latest_soil.p) if latest_soil.p else soil_p
            soil_k = float(latest_soil.k) if latest_soil.k else soil_k
            soil_moisture = float(latest_soil.moisture) if latest_soil.moisture else soil_moisture
        
        missing_data = []
        if soil_ph is None:
            missing_data.append('pH')
        if soil_n is None:
            missing_data.append('Nitrogen')
        if soil_p is None:
            missing_data.append('Phosphorus')
        if soil_k is None:
            missing_data.append('Potassium')
        
        if missing_data:
            logger.warning(
                f"Field '{field.name}' (ID: {field.id}) is missing soil data: {', '.join(missing_data)}. "
                f"Recommendations may be less accurate. Location: ({latitude}, {longitude})"
            )
        
        recommendations = cls.get_recommendations(
            soil_ph=soil_ph,
            soil_n=soil_n,
            soil_p=soil_p,
            soil_k=soil_k,
            soil_moisture=soil_moisture,
            temperature=temperature,
            rainfall=rainfall,
            humidity=humidity,
            latitude=latitude,
            longitude=longitude,
            limit=limit * 3,  # Fetch extra for composite ranking and filtering
            use_ml=use_ml
        )
        
        if BUSINESS_LOGIC_AVAILABLE and recommendations:
            from apps.farms.models import CropHistory
            crop_history = CropHistory.objects.filter(field=field).order_by('-year', '-season')
            field_history = [
                {
                    'crop_name': ch.crop_name,
                    'year': ch.year,
                    'season': ch.season
                }
                for ch in crop_history
            ]
            
            enhanced_recommendations = []
            max_profit = max((r.get('profit_margin', 0) for r in recommendations), default=1)
            
            for rec in recommendations:
                crop_name = rec['crop_name']
                
                rotation_analysis = CropRotationAnalyzer.get_rotation_score(
                    crop_name=crop_name,
                    field_history=field_history
                )
                
                risk_factor = ProfitCalculator.RISK_FACTORS.get(crop_name, 0.3)
                
                profit_score = RecommendationRanker.normalize_profit_for_scoring(
                    rec.get('profit_margin', 0),
                    max_profit=max_profit
                )
                yield_potential_score = RecommendationRanker.normalize_yield_for_scoring(
                    crop_name,
                    rec.get('expected_yield', 0)
                )
                
                composite_score_data = RecommendationRanker.calculate_composite_score(
                    compatibility_score=rec.get('confidence_score', 0),
                    profit_score=profit_score,
                    sustainability_score=rec.get('sustainability_score', 0),
                    rotation_score=rotation_analysis['rotation_score'],
                    yield_potential_score=yield_potential_score,
                    risk_factor=risk_factor
                )
                
                rec['rotation_analysis'] = rotation_analysis
                rec['composite_score'] = composite_score_data['composite_score']
                rec['composite_breakdown'] = composite_score_data['breakdown']
                rec['rotation_score'] = rotation_analysis['rotation_score']
                
                if rotation_analysis['reasons']:
                    rec['reasons'].extend(rotation_analysis['reasons'])
                
                enhanced_recommendations.append(rec)
            
            enhanced_recommendations.sort(
                key=lambda x: x.get('composite_score', x.get('confidence_score', 0)),
                reverse=True
            )
            
            if missing_data:
                for rec in enhanced_recommendations:
                    rec['missing_soil_data'] = missing_data
                    rec['data_quality_warning'] = f"Recommendations based on estimated soil data. Missing: {', '.join(missing_data)}"
            
            return enhanced_recommendations[:limit]
        
        if missing_data:
            for rec in recommendations:
                rec['missing_soil_data'] = missing_data
                rec['data_quality_warning'] = f"Recommendations based on estimated soil data. Missing: {', '.join(missing_data)}"
        
        return recommendations[:limit]

