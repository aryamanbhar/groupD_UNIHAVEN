from django.conf import settings
import requests

class GeoCodingService:
    @staticmethod
    def get_coordinates(address):
        """
        Fetches latitude and longitude for a given address using a geocoding API.
        """
        api_url = f"https://api.geocoding.example.com/v1/geocode?address={address}&key={settings.GEOCODING_API_KEY}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return {
                    'latitude': data['results'][0]['geometry']['location']['lat'],
                    'longitude': data['results'][0]['geometry']['location']['lng']
                }
        return None