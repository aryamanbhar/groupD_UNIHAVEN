import requests
from urllib.parse import quote

class GeoCodingService:
    ALS_ENDPOINT = "https://www.als.gov.hk/lookup"
    
    @classmethod
    def get_coordinates(cls, address):
        """
        Fetch latitude and longitude from the Hong Kong government address lookup service.
        Returns format: {'longitude': 114.123, 'latitude': 22.456, 'geo_address': '...'}
        """
        try:
            headers = {
                'Accept': 'application/json',
                'Accept-Language': 'en'  # Get English address information
            }
            params = {
                'q': quote(address),
                'n': '1'  # Fetch only the first matching result
            }
            
            response = requests.get(
                cls.ALS_ENDPOINT,
                headers=headers,
                params=params,
                timeout=5  # 5-second timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return cls._extract_location_data(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Geocoding API request failed: {e}")
        return None
    
    @classmethod
    def _extract_location_data(cls, data):
        """Extract location information from API response."""
        try:
            suggested_address = data.get('SuggestedAddress', [{}])[0]
            premises_address = suggested_address.get('Address', {}).get('PremisesAddress', {})
            geo_info = premises_address.get('GeospatialInformation', {})
            
            return {
                'longitude': float(geo_info.get('Longitude')),
                'latitude': float(geo_info.get('Latitude')),
                'geo_address': premises_address.get('GeoAddress'),
                'northing': geo_info.get('Northing'),
                'easting': geo_info.get('Easting')
            }
        except (KeyError, ValueError, IndexError):
            return None
