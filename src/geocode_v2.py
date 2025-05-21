# src/geocode.py

import requests
from src.config_v2 import BUHVAN_GEOCODE_URL, OSM_NOMINATIM_URL

def geocode_place(place_name: str) -> tuple[float, float]:
    """
    Resolve a place name to (latitude, longitude).
    1. Try ISRO Bhuvan’s place-lookup API.
    2. If that fails or returns no results, fall back to OpenStreetMap Nominatim.
    
    Returns:
        (latitude, longitude)
    
    Raises:
        ValueError if neither service returns a location.
    """
    # 1. Try Bhuvan
    try:
        resp = requests.get(
            BUHVAN_GEOCODE_URL,
            params={'placename': place_name},
            timeout=5
        )
        resp.raise_for_status()
        data = resp.json()
        # Bhuvan’s JSON typically has a "results" list of dicts
        if isinstance(data, dict) and 'results' in data and data['results']:
            first = data['results'][0]
            lat = float(first.get('Latitude') or first.get('latitude'))
            lon = float(first.get('Longitude') or first.get('longitude'))
            return lat, lon
    except Exception:
        # silently fall through to OSM
        pass

    # 2. Fallback to OSM Nominatim
    osm_resp = requests.get(
        OSM_NOMINATIM_URL,
        params={'q': place_name, 'format': 'json', 'limit': 1},
        headers={'User-Agent': 'map-console/1.0'},
        timeout=5
    )
    osm_resp.raise_for_status()
    osm_data = osm_resp.json()
    if osm_data:
        lat = float(osm_data[0]['lat'])
        lon = float(osm_data[0]['lon'])
        return lat, lon

    raise ValueError(f"Could not geocode place: {place_name}")
