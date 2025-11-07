"""
Soil data API integration services.
Handles fetching soil data from various sources (Soil Grids, Bhuvan, manual input).
"""
import requests
import logging
from typing import Dict, Optional, Tuple
from decimal import Decimal
from django.conf import settings

logger = logging.getLogger(__name__)


class SoilDataService:
    """Service for fetching and processing soil data from various sources."""
    
    @staticmethod
    def fetch_soil_grids_data(latitude: float, longitude: float) -> Optional[Dict]:
        """
        Fetch soil data from Soil Grids API.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dictionary with soil data or None if failed
        """
        try:
            # Soil Grids API endpoint
            # Note: This is a placeholder - actual API endpoint may vary
            # Soil Grids uses WCS (Web Coverage Service) protocol
            base_url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
            
            params = {
                'lon': longitude,
                'lat': latitude,
                'property': 'phh2o,ocd,sand,clay,bdod,cec',
                'depth': '0-5cm',
                'value': 'mean'
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract and process soil properties
                properties = data.get('properties', {})
                
                # Convert Soil Grids data to our format
                # Note: Soil Grids returns different units, need conversion
                soil_data = {
                    'ph': SoilDataService._extract_property(properties, 'phh2o', 'mean') / 10.0,  # Convert from 0-100 to 0-10
                    'moisture': None,  # Soil Grids doesn't provide moisture directly
                    'n': None,  # Need to calculate from organic carbon
                    'p': None,  # Not directly available
                    'k': None,  # Not directly available
                    'organic_carbon': SoilDataService._extract_property(properties, 'ocd', 'mean'),
                    'sand': SoilDataService._extract_property(properties, 'sand', 'mean'),
                    'clay': SoilDataService._extract_property(properties, 'clay', 'mean'),
                    'bulk_density': SoilDataService._extract_property(properties, 'bdod', 'mean') / 100.0,
                    'cec': SoilDataService._extract_property(properties, 'cec', 'mean'),
                }
                
                # Estimate N from organic carbon (rough approximation)
                if soil_data['organic_carbon']:
                    # Organic carbon to nitrogen ratio is typically 10:1 to 12:1
                    soil_data['n'] = soil_data['organic_carbon'] * 0.1
                
                return soil_data
            else:
                logger.warning(f"Soil Grids API returned status {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Soil Grids data: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in Soil Grids fetch: {str(e)}")
            return None
    
    @staticmethod
    def fetch_bhuvan_data(latitude: float, longitude: float) -> Optional[Dict]:
        """
        Fetch soil data from Bhuvan API (for Indian regions).
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dictionary with soil data or None if failed
        """
        try:
            # Bhuvan API endpoint
            # Note: This is a placeholder - actual API endpoint and authentication may be required
            base_url = "https://bhuvan-app1.nrsc.gov.in/api/soil"
            
            params = {
                'lat': latitude,
                'lon': longitude,
                'format': 'json'
            }
            
            # Add API key if available
            api_key = getattr(settings, 'BHUVAN_API_KEY', None)
            if api_key:
                params['api_key'] = api_key
            
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract and process Bhuvan soil data
                # Note: Actual structure depends on Bhuvan API response
                soil_data = {
                    'ph': data.get('ph'),
                    'moisture': data.get('moisture'),
                    'n': data.get('nitrogen'),
                    'p': data.get('phosphorus'),
                    'k': data.get('potassium'),
                }
                
                return soil_data
            else:
                logger.warning(f"Bhuvan API returned status {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Bhuvan data: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in Bhuvan fetch: {str(e)}")
            return None
    
    @staticmethod
    def get_soil_data(latitude: float, longitude: float, source: str = 'auto') -> Optional[Dict]:
        """
        Get soil data from the best available source.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            source: Data source preference ('auto', 'soil_grids', 'bhuvan', 'manual')
            
        Returns:
            Dictionary with soil data or None if failed
        """
        # Check if coordinates are in India (rough bounds)
        is_india = 6.0 <= latitude <= 37.0 and 68.0 <= longitude <= 97.0
        
        if source == 'auto':
            # Try Bhuvan first for India, otherwise Soil Grids
            if is_india:
                data = SoilDataService.fetch_bhuvan_data(latitude, longitude)
                if data:
                    data['source'] = 'bhuvan'
                    return data
            
            # Try Soil Grids
            data = SoilDataService.fetch_soil_grids_data(latitude, longitude)
            if data:
                data['source'] = 'soil_grids'
                return data
            
            return None
        
        elif source == 'soil_grids':
            data = SoilDataService.fetch_soil_grids_data(latitude, longitude)
            if data:
                data['source'] = 'soil_grids'
            return data
        
        elif source == 'bhuvan':
            data = SoilDataService.fetch_bhuvan_data(latitude, longitude)
            if data:
                data['source'] = 'bhuvan'
            return data
        
        return None
    
    @staticmethod
    def _extract_property(properties: Dict, key: str, stat: str = 'mean') -> Optional[float]:
        """Extract property value from Soil Grids response."""
        try:
            prop_data = properties.get(key, {})
            if isinstance(prop_data, dict):
                return prop_data.get(stat)
            return prop_data
        except (KeyError, TypeError, AttributeError):
            return None
    
    @staticmethod
    def validate_soil_data(data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate soil data values.
        
        Args:
            data: Dictionary with soil data
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate pH (typically 0-14)
        if 'ph' in data and data['ph'] is not None:
            ph = float(data['ph'])
            if not (0 <= ph <= 14):
                return False, "pH must be between 0 and 14"
        
        # Validate moisture (typically 0-100%)
        if 'moisture' in data and data['moisture'] is not None:
            moisture = float(data['moisture'])
            if not (0 <= moisture <= 100):
                return False, "Moisture must be between 0 and 100"
        
        # Validate nutrients (should be positive)
        for nutrient in ['n', 'p', 'k']:
            if nutrient in data and data[nutrient] is not None:
                value = float(data[nutrient])
                if value < 0:
                    return False, f"{nutrient.upper()} must be non-negative"
        
        return True, None

