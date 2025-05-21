# src/config_v4.py

# ISRO Bhuvan OGC WMS settings
WMS_URL = "https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms"
WMS_VERSION = "1.3.0"

# Default map settings
DEFAULT_CENTER = (20.5937, 78.9629)  # Approximate center of India
DEFAULT_ZOOM = 5

# Define reliable external basemaps
EXTERNAL_BASEMAPS = {
    "OpenStreetMap": {
        "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "attribution": "© OpenStreetMap contributors"
    },
    "ESRI Satellite": {
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "attribution": "© Esri, Maxar, Earthstar Geographics, and the GIS User Community"
    },
    "ESRI Terrain": {
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
        "attribution": "© Esri, USGS, FAO, NOAA"
    }
}

# Map layers configuration
BHUVAN_LAYERS = {
    # Base layers
    "OpenStreetMap": {"type": "tile", "name": "OpenStreetMap"},
    "ESRI Satellite": {"type": "external_tile", "name": "ESRI Satellite"},
    "ESRI Terrain": {"type": "external_tile", "name": "ESRI Terrain"},
    
    # Overlay layers
    "State Boundaries": {"type": "wms", "name": "admin:INDIA_STATE", "overlay": True, "url": WMS_URL},
    "District Boundaries": {"type": "wms", "name": "admin:INDIA_DIST_250K", "overlay": True, "url": WMS_URL},
    "Rivers": {"type": "wms", "name": "disaster:godavari_Rivers", "overlay": True, "url": WMS_URL}
}

# Default active layers
DEFAULT_BASE_LAYER = "ESRI Satellite"
DEFAULT_OVERLAYS = []

# Unit conversion factors (from m²)
UNITS = {
    "km2": 1e-6,    # square metres → square kilometres
    "ha": 1e-4,     # square metres → hectares
    "m2": 1.0       # square metres
}

# Search simulation parameters
DEFAULT_DRONES = 5
MAX_SIMULATION_STEPS = 100
DRONE_COLORS = [
    "#3498db",  # Blue
    "#e74c3c",  # Red
    "#2ecc71",  # Green
    "#f39c12",  # Orange
    "#9b59b6",  # Purple
    "#1abc9c",  # Turquoise
    "#d35400",  # Pumpkin
    "#2c3e50",  # Dark Blue
    "#27ae60",  # Dark Green
    "#c0392b"   # Dark Red
]