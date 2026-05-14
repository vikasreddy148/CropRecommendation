"""
Enhanced Business Logic for Crop Recommendations.

This module provides sophisticated business logic for:
- Crop rotation analysis
- Profit calculation with input costs
- Dynamic sustainability scoring
- Multi-factor recommendation ranking
"""
import logging
from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict

logger = logging.getLogger(__name__)


class CropRotationAnalyzer:
    """Analyzes crop rotation history and provides rotation recommendations."""
    
    # Crop families for rotation analysis
    CROP_FAMILIES = {
        'Rice': 'cereal',
        'Wheat': 'cereal',
        'Maize': 'cereal',
        'Soybean': 'legume',
        'Groundnut': 'legume',
        'Pigeon Pea': 'legume',
        'Cotton': 'fiber',
        'Sugarcane': 'cash',
        'Potato': 'root',
        'Tomato': 'solanaceae',
        'Onion': 'allium',
        'Chilli': 'solanaceae',
        'Chickpea': 'legume',
        'Kidneybeans': 'legume',
        'Mothbeans': 'legume',
        'Mungbean': 'legume',
        'Blackgram': 'legume',
        'Lentil': 'legume',
        'Apple': 'fruit',
        'Banana': 'fruit',
        'Mango': 'fruit',
        'Grapes': 'fruit',
        'Orange': 'fruit',
        'Papaya': 'fruit',
        'Pomegranate': 'fruit',
        'Watermelon': 'fruit',
        'Muskmelon': 'fruit',
        'Coconut': 'fruit',
        'Jute': 'fiber',
        'Coffee': 'cash',
    }
    
    # Crop compatibility matrix (crops that work well together in rotation)
    COMPATIBLE_ROTATIONS = {
        'Rice': ['Wheat', 'Potato', 'Groundnut', 'Soybean'],
        'Wheat': ['Rice', 'Soybean', 'Groundnut', 'Potato'],
        'Maize': ['Soybean', 'Groundnut', 'Wheat'],
        'Soybean': ['Wheat', 'Rice', 'Maize', 'Cotton'],
        'Groundnut': ['Wheat', 'Rice', 'Maize'],
        'Cotton': ['Wheat', 'Soybean', 'Groundnut'],
        'Potato': ['Wheat', 'Rice', 'Soybean'],
        'Tomato': ['Wheat', 'Onion', 'Groundnut'],
        'Onion': ['Wheat', 'Tomato', 'Potato'],
        'Chilli': ['Wheat', 'Onion', 'Groundnut'],
        'Pigeon Pea': ['Wheat', 'Rice', 'Cotton'],
        'Sugarcane': ['Wheat', 'Potato', 'Groundnut'],
        'Chickpea': ['Wheat', 'Rice', 'Maize'],
        'Kidneybeans': ['Wheat', 'Maize'],
        'Mothbeans': ['Wheat', 'Maize'],
        'Mungbean': ['Wheat', 'Rice', 'Maize'],
        'Blackgram': ['Wheat', 'Rice', 'Maize'],
        'Lentil': ['Wheat', 'Rice', 'Maize'],
    }
    
    # Crops that should not be grown consecutively (same family or incompatible)
    INCOMPATIBLE_CROPS = {
        'Rice': ['Rice'],  # Avoid same crop
        'Wheat': ['Wheat'],
        'Maize': ['Maize', 'Rice', 'Wheat'],  # Same family
        'Tomato': ['Tomato', 'Chilli', 'Potato'],  # Same family
        'Chilli': ['Chilli', 'Tomato', 'Potato'],
        'Potato': ['Potato', 'Tomato', 'Chilli'],
    }
    
    @classmethod
    def get_rotation_score(
        cls,
        crop_name: str,
        field_history: List[Dict],
        years_to_check: int = 3
    ) -> Dict:
        """
        Calculate rotation score for a crop based on field history.
        
        Args:
            crop_name: Name of the crop to evaluate
            field_history: List of dicts with 'crop_name', 'year', 'season' keys
            years_to_check: Number of years to look back
            
        Returns:
            Dict with rotation_score (0-100), reasons, and rotation_benefits
        """
        if not field_history:
            return {
                'rotation_score': 100,
                'reasons': ['No crop history - rotation score neutral'],
                'rotation_benefits': [],
                'rotation_penalties': []
            }
        
        current_year = timezone.now().year
        recent_history = [
            h for h in field_history
            if h.get('year', 0) >= (current_year - years_to_check)
        ]
        
        if not recent_history:
            return {
                'rotation_score': 100,
                'reasons': ['No recent crop history - rotation score neutral'],
                'rotation_benefits': [],
                'rotation_penalties': []
            }
        
        score = 100
        reasons = []
        benefits = []
        penalties = []
        
        # Check for same crop in recent history
        same_crop_count = sum(1 for h in recent_history if h.get('crop_name') == crop_name)
        if same_crop_count > 0:
            penalty = min(same_crop_count * 25, 50)  # Max 50 point penalty
            score -= penalty
            penalties.append(f'Crop {crop_name} was grown {same_crop_count} time(s) in last {years_to_check} years')
            reasons.append(f'Crop rotation: {crop_name} grown recently - {penalty}% penalty')
        
        # Check for incompatible crops
        crop_family = cls.CROP_FAMILIES.get(crop_name, 'unknown')
        incompatible_crops = cls.INCOMPATIBLE_CROPS.get(crop_name, [])
        
        for history_item in recent_history:
            prev_crop = history_item.get('crop_name')
            if prev_crop in incompatible_crops:
                score -= 15
                penalties.append(f'Incompatible crop {prev_crop} grown recently')
                reasons.append(f'Crop rotation: {prev_crop} is incompatible with {crop_name}')
        
        # Check for compatible rotations (bonus)
        compatible_crops = cls.COMPATIBLE_ROTATIONS.get(crop_name, [])
        for history_item in recent_history:
            prev_crop = history_item.get('crop_name')
            if prev_crop in compatible_crops:
                score += 10
                benefits.append(f'Good rotation: {prev_crop} → {crop_name}')
                reasons.append(f'Crop rotation: Good rotation from {prev_crop}')
        
        # Legume bonus (nitrogen fixing)
        if crop_family == 'legume':
            # Check if previous crop was not a legume
            has_non_legume = any(
                cls.CROP_FAMILIES.get(h.get('crop_name'), '') != 'legume'
                for h in recent_history
            )
            if has_non_legume:
                score += 5
                benefits.append('Legume crop after non-legume improves soil nitrogen')
                reasons.append('Crop rotation: Legume crop benefits soil health')
        
        # Ensure score stays within bounds
        score = max(0, min(100, score))
        
        if score >= 90:
            reasons.insert(0, 'Excellent crop rotation pattern')
        elif score >= 70:
            reasons.insert(0, 'Good crop rotation pattern')
        elif score >= 50:
            reasons.insert(0, 'Moderate crop rotation - some improvements recommended')
        else:
            reasons.insert(0, 'Poor crop rotation - significant improvements needed')
        
        return {
            'rotation_score': round(score, 2),
            'reasons': reasons,
            'rotation_benefits': benefits,
            'rotation_penalties': penalties
        }


class ProfitCalculator:
    """Enhanced profit calculator with input costs and market prices."""
    
    # Average market prices per kg (in local currency - approximate)
    MARKET_PRICES = {
        'Rice': 25,
        'Wheat': 22,
        'Maize': 18,
        'Cotton': 120,
        'Sugarcane': 3,
        'Potato': 15,
        'Tomato': 30,
        'Onion': 20,
        'Chilli': 80,
        'Groundnut': 60,
        'Soybean': 45,
        'Pigeon Pea': 50,
        'Chickpea': 45,
        'Kidneybeans': 60,
        'Mothbeans': 40,
        'Mungbean': 55,
        'Blackgram': 60,
        'Lentil': 50,
        'Apple': 150,
        'Banana': 20,
        'Mango': 80,
        'Grapes': 100,
        'Orange': 40,
        'Papaya': 25,
        'Pomegranate': 120,
        'Watermelon': 15,
        'Muskmelon': 20,
        'Coconut': 30,
        'Jute': 45,
        'Coffee': 200,
    }
    
    # Input costs per hectare (seeds, fertilizers, pesticides, labor, etc.)
    INPUT_COSTS = {
        'Rice': 40000,
        'Wheat': 35000,
        'Maize': 38000,
        'Cotton': 50000,
        'Sugarcane': 60000,
        'Potato': 80000,
        'Tomato': 100000,
        'Onion': 70000,
        'Chilli': 90000,
        'Groundnut': 45000,
        'Soybean': 40000,
        'Pigeon Pea': 35000,
        'Chickpea': 30000,
        'Kidneybeans': 35000,
        'Mothbeans': 25000,
        'Mungbean': 30000,
        'Blackgram': 32000,
        'Lentil': 28000,
        'Apple': 150000,
        'Banana': 80000,
        'Mango': 100000,
        'Grapes': 120000,
        'Orange': 90000,
        'Papaya': 70000,
        'Pomegranate': 110000,
        'Watermelon': 40000,
        'Muskmelon': 45000,
        'Coconut': 60000,
        'Jute': 35000,
        'Coffee': 180000,
    }
    
    # Labor costs per hectare (additional to input costs)
    LABOR_COSTS = {
        'Rice': 20000,
        'Wheat': 15000,
        'Maize': 18000,
        'Cotton': 25000,
        'Sugarcane': 30000,
        'Potato': 25000,
        'Tomato': 30000,
        'Onion': 20000,
        'Chilli': 25000,
        'Groundnut': 20000,
        'Soybean': 18000,
        'Pigeon Pea': 15000,
        'Chickpea': 12000,
        'Kidneybeans': 15000,
        'Mothbeans': 10000,
        'Mungbean': 12000,
        'Blackgram': 14000,
        'Lentil': 12000,
        'Apple': 50000,
        'Banana': 30000,
        'Mango': 40000,
        'Grapes': 60000,
        'Orange': 35000,
        'Papaya': 25000,
        'Pomegranate': 45000,
        'Watermelon': 15000,
        'Muskmelon': 18000,
        'Coconut': 20000,
        'Jute': 20000,
        'Coffee': 100000,
    }
    
    # Risk factors (0-1, where 1 is highest risk)
    RISK_FACTORS = {
        'Rice': 0.3,  # Weather dependent
        'Wheat': 0.2,
        'Maize': 0.25,
        'Cotton': 0.4,  # Pest prone
        'Sugarcane': 0.2,
        'Potato': 0.35,  # Disease prone
        'Tomato': 0.4,  # Perishable
        'Onion': 0.3,
        'Chilli': 0.35,
        'Groundnut': 0.25,
        'Soybean': 0.2,
        'Pigeon Pea': 0.2,
        'Chickpea': 0.2,
        'Kidneybeans': 0.25,
        'Mothbeans': 0.3,
        'Mungbean': 0.2,
        'Blackgram': 0.25,
        'Lentil': 0.2,
        'Apple': 0.4,
        'Banana': 0.3,
        'Mango': 0.35,
        'Grapes': 0.4,
        'Orange': 0.3,
        'Papaya': 0.35,
        'Pomegranate': 0.3,
        'Watermelon': 0.25,
        'Muskmelon': 0.3,
        'Coconut': 0.2,
        'Jute': 0.25,
        'Coffee': 0.3,
    }
    
    @classmethod
    def calculate_profit(
        cls,
        crop_name: str,
        expected_yield: float,
        yield_multiplier: float = 1.0,
        risk_adjustment: float = 1.0,
        compatibility_score: float = 100.0
    ) -> Dict:
        """
        Calculate profit with detailed breakdown.
        
        Args:
            crop_name: Name of the crop
            expected_yield: Expected yield in kg/hectare
            yield_multiplier: Multiplier based on conditions (0-1)
            risk_adjustment: Risk adjustment factor (0-1)
            compatibility_score: Agronomic compatibility score (0-100)
            
        Returns:
            Dict with profit details
        """
        # Get base values
        market_price = cls.MARKET_PRICES.get(crop_name, 20)
        input_cost = cls.INPUT_COSTS.get(crop_name, 40000)
        labor_cost = cls.LABOR_COSTS.get(crop_name, 20000)
        risk_factor = cls.RISK_FACTORS.get(crop_name, 0.3)
        
        # Expected yield is already FinalYield, but apply multiplier if needed
        adjusted_yield = expected_yield * yield_multiplier
        
        # Revenue = FinalYield × MarketPrice
        revenue = adjusted_yield * market_price
        
        # Total Production Costs
        total_costs = input_cost + labor_cost
        
        # Profit = Revenue − ProductionCost
        gross_profit = revenue - total_costs
        
        # Calculate uncertainty factor based on low compatibility
        uncertainty_factor = max(0.0, min(1.0, 1.0 - (compatibility_score / 100.0)))
        
        # Apply risk and uncertainty adjustments correctly
        if gross_profit > 0:
            # Reduce profit by risk factor and uncertainty
            risk_adjusted_profit = gross_profit * (1 - risk_factor * risk_adjustment) * (1 - uncertainty_factor * 0.4)
        else:
            # Amplify loss by risk factor and uncertainty
            risk_adjusted_profit = gross_profit * (1 + risk_factor * risk_adjustment) * (1 + uncertainty_factor * 0.4)
        
        # Calculate profit margin percentage
        profit_margin_pct = (risk_adjusted_profit / revenue * 100) if revenue > 0 else 0
        
        # ROI = (Profit / ProductionCost) × 100
        roi = (risk_adjusted_profit / total_costs * 100) if total_costs > 0 else 0
        
        return {
            'crop_name': crop_name,
            'expected_yield': round(adjusted_yield, 2),
            'market_price_per_kg': market_price,
            'revenue': round(revenue, 2),
            'input_costs': input_cost,
            'labor_costs': labor_cost,
            'total_costs': total_costs,
            'gross_profit': round(gross_profit, 2),
            'risk_factor': risk_factor,
            'risk_factor_percentage': round(risk_factor * 100, 1),
            'uncertainty_factor': round(uncertainty_factor, 2),
            'confidence_score': round(compatibility_score, 1),
            'risk_adjusted_profit': round(risk_adjusted_profit, 2),
            'profit_margin': round(risk_adjusted_profit, 2),  # For backward compatibility
            'profit_margin_percentage': round(profit_margin_pct, 2),
            'roi': round(roi, 2),
            'breakdown': {
                'revenue': round(revenue, 2),
                'costs': {
                    'inputs': input_cost,
                    'labor': labor_cost,
                    'total': total_costs
                },
                'profit': round(risk_adjusted_profit, 2)
            }
        }


class SustainabilityScorer:
    """Dynamic sustainability scoring based on multiple factors."""
    
    # Water usage per hectare (liters)
    WATER_USAGE = {
        'Rice': 2500000,  # Very high
        'Wheat': 800000,
        'Maize': 600000,
        'Cotton': 1000000,
        'Sugarcane': 2000000,
        'Potato': 500000,
        'Tomato': 600000,
        'Onion': 400000,
        'Chilli': 500000,
        'Groundnut': 500000,
        'Soybean': 600000,
        'Pigeon Pea': 400000,
        'Chickpea': 450000,
        'Kidneybeans': 500000,
        'Mothbeans': 300000,
        'Mungbean': 400000,
        'Blackgram': 450000,
        'Lentil': 400000,
        'Apple': 1200000,
        'Banana': 1500000,
        'Mango': 1000000,
        'Grapes': 1200000,
        'Orange': 1000000,
        'Papaya': 800000,
        'Pomegranate': 700000,
        'Watermelon': 600000,
        'Muskmelon': 500000,
        'Coconut': 1800000,
        'Jute': 1500000,
        'Coffee': 1200000,
    }
    
    # Soil health impact (-100 to +100, positive is good)
    SOIL_HEALTH_IMPACT = {
        'Rice': -10,  # Can cause soil compaction
        'Wheat': 0,
        'Maize': -5,
        'Cotton': -20,  # High pesticide use
        'Sugarcane': -15,
        'Potato': -10,
        'Tomato': -5,
        'Onion': 0,
        'Chilli': -5,
        'Groundnut': 20,  # Nitrogen fixing
        'Soybean': 25,  # Nitrogen fixing
        'Pigeon Pea': 30,  # Nitrogen fixing, deep roots
        'Chickpea': 25,
        'Kidneybeans': 20,
        'Mothbeans': 20,
        'Mungbean': 25,
        'Blackgram': 25,
        'Lentil': 25,
        'Apple': 10,
        'Banana': 5,
        'Mango': 15,
        'Grapes': 10,
        'Orange': 10,
        'Papaya': 5,
        'Pomegranate': 15,
        'Watermelon': 5,
        'Muskmelon': 5,
        'Coconut': 20,
        'Jute': -5,
        'Coffee': 10,
    }
    
    # Carbon footprint (kg CO2 per hectare)
    CARBON_FOOTPRINT = {
        'Rice': 5000,  # Methane emissions
        'Wheat': 2000,
        'Maize': 2500,
        'Cotton': 4000,
        'Sugarcane': 3000,
        'Potato': 2500,
        'Tomato': 3000,
        'Onion': 2000,
        'Chilli': 2500,
        'Groundnut': 1500,
        'Soybean': 1500,
        'Pigeon Pea': 1000,
        'Chickpea': 1200,
        'Kidneybeans': 1500,
        'Mothbeans': 1200,
        'Mungbean': 1300,
        'Blackgram': 1400,
        'Lentil': 1200,
        'Apple': 2500,
        'Banana': 3000,
        'Mango': 2000,
        'Grapes': 2500,
        'Orange': 2200,
        'Papaya': 2400,
        'Pomegranate': 2000,
        'Watermelon': 1800,
        'Muskmelon': 1800,
        'Coconut': 1500,
        'Jute': 3000,
        'Coffee': 3500,
    }
    
    # Biodiversity impact (-100 to +100)
    BIODIVERSITY_IMPACT = {
        'Rice': 10,  # Supports wetland ecosystems
        'Wheat': 0,
        'Maize': -10,
        'Cotton': -30,
        'Sugarcane': -20,
        'Potato': -5,
        'Tomato': 0,
        'Onion': 0,
        'Chilli': 0,
        'Groundnut': 10,
        'Soybean': 15,
        'Pigeon Pea': 20,
        'Chickpea': 15,
        'Kidneybeans': 10,
        'Mothbeans': 10,
        'Mungbean': 15,
        'Blackgram': 15,
        'Lentil': 15,
        'Apple': 20,
        'Banana': 25,
        'Mango': 40,
        'Grapes': 30,
        'Orange': 35,
        'Papaya': 25,
        'Pomegranate': 30,
        'Watermelon': 15,
        'Muskmelon': 15,
        'Coconut': 50,
        'Jute': 20,
        'Coffee': 40,
    }
    
    @classmethod
    def calculate_sustainability_score(
        cls,
        crop_name: str,
        water_availability: Optional[float] = None,
        soil_health_bonus: float = 0.0,
        rotation_bonus: float = 0.0
    ) -> Dict:
        """
        Calculate dynamic sustainability score.
        
        Args:
            crop_name: Name of the crop
            water_availability: Available water (liters/hectare), None if unknown
            soil_health_bonus: Bonus from crop rotation (0-20)
            rotation_bonus: Additional bonus from good rotation (0-10)
            
        Returns:
            Dict with sustainability score and breakdown
        """
        base_score = 50  # Start with neutral score
        
        # Water usage score (0-25 points)
        water_usage = cls.WATER_USAGE.get(crop_name, 1000000)
        if water_availability is not None:
            if water_availability >= water_usage * 1.2:
                water_score = 25  # Plenty of water
            elif water_availability >= water_usage:
                water_score = 20  # Sufficient water
            elif water_availability >= water_usage * 0.8:
                water_score = 15  # Moderate water
            else:
                water_score = 5  # Low water
        else:
            # Unknown water availability - use crop's water efficiency
            if water_usage < 500000:
                water_score = 20  # Low water usage
            elif water_usage < 1000000:
                water_score = 15  # Moderate water usage
            else:
                water_score = 10  # High water usage
        
        # Soil health score (0-25 points)
        soil_impact = cls.SOIL_HEALTH_IMPACT.get(crop_name, 0)
        soil_score = 12.5 + (soil_impact / 2)  # Convert -100 to +100 scale to 0-25
        soil_score = max(0, min(25, soil_score))
        soil_score += soil_health_bonus  # Add rotation bonus
        
        # Carbon footprint score (0-25 points)
        carbon_footprint = cls.CARBON_FOOTPRINT.get(crop_name, 3000)
        if carbon_footprint < 1500:
            carbon_score = 25  # Very low
        elif carbon_footprint < 2500:
            carbon_score = 20  # Low
        elif carbon_footprint < 3500:
            carbon_score = 15  # Moderate
        else:
            carbon_score = 10  # High
        
        # Biodiversity score (0-25 points)
        biodiversity_impact = cls.BIODIVERSITY_IMPACT.get(crop_name, 0)
        biodiversity_score = 12.5 + (biodiversity_impact / 2)  # Convert to 0-25 scale
        biodiversity_score = max(0, min(25, biodiversity_score))
        biodiversity_score += rotation_bonus  # Add rotation bonus
        
        # Calculate total score
        total_score = water_score + soil_score + carbon_score + biodiversity_score
        total_score = max(0, min(100, total_score))
        
        return {
            'sustainability_score': round(total_score, 2),
            'breakdown': {
                'water_score': round(water_score, 2),
                'water_score_percentage': round((water_score / 25) * 100, 1),  # For progress bar width
                'soil_score': round(soil_score, 2),
                'soil_score_percentage': round((soil_score / 25) * 100, 1),  # For progress bar width
                'carbon_score': round(carbon_score, 2),
                'carbon_score_percentage': round((carbon_score / 25) * 100, 1),  # For progress bar width
                'biodiversity_score': round(biodiversity_score, 2),
                'biodiversity_score_percentage': round((biodiversity_score / 25) * 100, 1),  # For progress bar width
            },
            'factors': {
                'water_usage': water_usage,
                'soil_health_impact': soil_impact,
                'carbon_footprint': carbon_footprint,
                'biodiversity_impact': biodiversity_impact
            }
        }


class RecommendationRanker:
    """Multi-factor ranking system for recommendations."""
    
    # Weight factors for different criteria
    WEIGHTS = {
        'compatibility': 0.35,     # Soil/weather compatibility
        'profit': 0.25,            # Profit potential
        'sustainability': 0.20,    # Sustainability score
        'rotation': 0.10,          # Crop rotation benefits
        'yield_potential': 0.10,   # Yield potential relative to optimal benchmark
    }
    
    @classmethod
    def calculate_composite_score(
        cls,
        compatibility_score: float,
        profit_score: float,
        sustainability_score: float,
        rotation_score: float,
        yield_potential_score: float,
        risk_factor: float = 0.3
    ) -> Dict:
        """
        Calculate composite score for ranking recommendations.
        
        Args:
            compatibility_score: 0-100
            profit_score: 0-100 (normalized profit)
            sustainability_score: 0-100
            rotation_score: 0-100
            yield_potential_score: 0-100
            risk_factor: 0-1 (for tracking, but weights use yield_potential)
            
        Returns:
            Dict with composite_score and breakdown
        """
        # Normalize scores (0-100)
        profit_normalized = min(100.0, max(0.0, profit_score))
        yield_normalized = min(100.0, max(0.0, yield_potential_score))
        
        # Calculate weighted composite score
        composite = (
            compatibility_score * cls.WEIGHTS['compatibility'] +
            profit_normalized * cls.WEIGHTS['profit'] +
            sustainability_score * cls.WEIGHTS['sustainability'] +
            rotation_score * cls.WEIGHTS['rotation'] +
            yield_normalized * cls.WEIGHTS['yield_potential']
        )
        
        return {
            'composite_score': round(composite, 2),
            'breakdown': {
                'compatibility': round(compatibility_score * cls.WEIGHTS['compatibility'], 2),
                'profit': round(profit_normalized * cls.WEIGHTS['profit'], 2),
                'sustainability': round(sustainability_score * cls.WEIGHTS['sustainability'], 2),
                'rotation': round(rotation_score * cls.WEIGHTS['rotation'], 2),
                'yield_potential': round(yield_normalized * cls.WEIGHTS['yield_potential'], 2)
            },
            'weights': cls.WEIGHTS
        }
    
    @classmethod
    def normalize_profit_for_scoring(cls, profit: float, max_profit: float = None) -> float:
        """
        Normalize profit value to 0-100 scale for scoring.
        """
        if profit <= 0:
            return 0
        
        if max_profit and max_profit > 0:
            return min(100.0, (profit / max_profit) * 100.0)
        else:
            if profit >= 200000:
                return 100
            elif profit >= 150000:
                return 85
            elif profit >= 100000:
                return 70
            elif profit >= 50000:
                return 50
            elif profit >= 25000:
                return 30
            else:
                return 15

    @classmethod
    def normalize_yield_for_scoring(cls, crop_name: str, expected_yield: float) -> float:
        """
        Normalize expected yield to 0-100 scale relative to crop's optimal benchmark.
        """
        from apps.recommendations.services import CropRecommendationService
        optimal_yield = CropRecommendationService.AVERAGE_YIELDS.get(crop_name, 1000) * 1.2
        if optimal_yield <= 0 or expected_yield <= 0:
            return 0.0
        return min(100.0, (expected_yield / optimal_yield) * 100.0)


class ExplainabilityGenerator:
    """Generates structured explainability and confidence insights for recommendations."""
    
    @classmethod
    def generate_explanation(
        cls,
        crop_name: str,
        compatibility_score: float,
        expected_yield: float,
        profit_margin: float,
        roi: float,
        reasons: List[str]
    ) -> Dict:
        """
        Generate structured explainability insights.
        """
        strengths = []
        risks = []
        
        # Analyze compatibility
        if compatibility_score >= 80:
            compat_expl = f"{crop_name} is highly compatible ({compatibility_score:.1f}%) with your soil and weather conditions."
            strengths.append("Optimal soil and weather compatibility")
        elif compatibility_score >= 50:
            compat_expl = f"{crop_name} has moderate compatibility ({compatibility_score:.1f}%) with your conditions."
        else:
            compat_expl = f"{crop_name} has poor compatibility ({compatibility_score:.1f}%) with current field conditions."
            risks.append("Severe agronomic mismatch with soil/climate")
            
        # Analyze profit/ROI
        if profit_margin > 100000 and roi > 50:
            strengths.append("High market profitability and strong return on investment")
        elif profit_margin < 25000:
            risks.append("Low profit margins relative to input costs")
            
        # Analyze confidence
        yield_conf = "High" if compatibility_score >= 70 else ("Moderate" if compatibility_score >= 40 else "Low")
        roi_conf = "High" if compatibility_score >= 70 else ("Moderate" if compatibility_score >= 40 else "Low")
        
        if compatibility_score < 40 and profit_margin > 50000:
            summary = f"{crop_name} has high market profitability but poor soil compatibility, reducing prediction confidence."
        elif compatibility_score >= 70 and profit_margin > 50000:
            summary = f"{crop_name} is an excellent recommendation combining high agronomic suitability with strong financial returns."
        elif compatibility_score >= 70:
            summary = f"{crop_name} is highly suitable agronomically, though financial returns are moderate."
        else:
            summary = f"{crop_name} is not recommended due to poor agronomic compatibility and high prediction uncertainty."
            
        return {
            "summary": summary,
            "strengths": strengths,
            "risks": risks,
            "compatibility_explanation": compat_expl,
            "yield_confidence": yield_conf,
            "roi_confidence": roi_conf
        }

