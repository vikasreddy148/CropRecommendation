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
            base_url = "https://rest.isric.org/soilgrids/v2.0/properties/query"
            
            # Query properties one at a time to avoid API errors
            properties_to_fetch = ['phh2o', 'ocd', 'sand', 'clay', 'bdod', 'cec']
            property_values = {}
            
            for prop in properties_to_fetch:
                # Ensure parameters are strings/floats as API expects
                params = {
                    'lon': float(longitude),
                    'lat': float(latitude),
                    'property': str(prop),
                    'depth': '0-5cm',
                    'value': 'mean'
                }
                
                try:
                    response = requests.get(base_url, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # Extract value from the actual API structure
                        value = SoilDataService._extract_property_from_layers(data, prop)
                        if value is not None:
                            property_values[prop] = value
                    else:
                        # Log more details for debugging
                        logger.warning(
                            f"Soil Grids API returned status {response.status_code} for {prop}. "
                            f"URL: {response.url}, Response: {response.text[:200]}"
                        )
                except requests.exceptions.RequestException as e:
                    logger.error(f"Request error fetching {prop}: {str(e)}")
                    continue
                except Exception as e:
                    logger.error(f"Error fetching {prop}: {str(e)}")
                    continue
            
            # If we got at least one property, process the data
            if property_values:
                # Convert Soil Grids data to our format
                # pH is stored as pH*10 (d_factor=10), so divide by 10
                ph_value = property_values.get('phh2o')
                ph = ph_value / 10.0 if ph_value is not None else None
                
                # Organic carbon (ocd) is in g/kg, convert to kg/ha (rough estimate)
                organic_carbon = property_values.get('ocd')
                
                # Estimate N from organic carbon (rough approximation)
                # Organic carbon to nitrogen ratio is typically 10:1 to 12:1
                n_value = None
                if organic_carbon is not None:
                    # Convert g/kg to kg/ha (assuming bulk density ~1.3 g/cm³ and depth 5cm)
                    # This is a rough estimate
                    n_value = organic_carbon * 0.1 * 1.3 * 5  # Very rough conversion
                
                soil_data = {
                    'ph': ph,
                    'moisture': None,  # Soil Grids doesn't provide moisture directly
                    'n': n_value,
                    'p': None,  # Not directly available from Soil Grids
                    'k': None,  # Not directly available from Soil Grids
                    'organic_carbon': organic_carbon,
                    'sand': property_values.get('sand'),
                    'clay': property_values.get('clay'),
                    'bulk_density': property_values.get('bdod', 0) / 100.0 if property_values.get('bdod') else None,  # Convert from cg/cm³ to g/cm³
                    'cec': property_values.get('cec'),
                }
                
                return soil_data
            else:
                logger.warning("No soil data retrieved from Soil Grids API")
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
        """Extract property value from Soil Grids response (legacy method)."""
        try:
            prop_data = properties.get(key, {})
            if isinstance(prop_data, dict):
                return prop_data.get(stat)
            return prop_data
        except (KeyError, TypeError, AttributeError):
            return None
    
    @staticmethod
    def _extract_property_from_layers(data: Dict, property_name: str) -> Optional[float]:
        """Extract property value from Soil Grids API response structure.
        
        The API returns: {
            "properties": {
                "layers": [{
                    "name": "phh2o",
                    "depths": [{
                        "values": {"mean": 63}
                    }]
                }]
            }
        }
        """
        try:
            properties = data.get('properties', {})
            layers = properties.get('layers', [])
            
            # Find the layer with matching property name
            for layer in layers:
                if layer.get('name') == property_name:
                    depths = layer.get('depths', [])
                    if depths:
                        # Get the first depth (0-5cm)
                        values = depths[0].get('values', {})
                        mean_value = values.get('mean')
                        return float(mean_value) if mean_value is not None else None
            
            return None
        except (KeyError, TypeError, AttributeError, ValueError) as e:
            logger.debug(f"Error extracting {property_name}: {str(e)}")
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

