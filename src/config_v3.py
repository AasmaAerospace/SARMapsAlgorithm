# src/config_v3.py

# ISRO Bhuvan OGC WMS settings
WMS_URL = "https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms"
WMS_VERSION = "1.3.0"

# Alternative URLs
BHUVAN_RASTER_URL = "https://bhuvan-ras1.nrsc.gov.in/bhuvan/wms"
BHUVAN_VEC_URL = "https://bhuvan-vec1.nrsc.gov.in/bhuvan/wms"

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
    },
    "ESRI Topo": {
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        "attribution": "© Esri, USGS, NOAA"
    },
    "CartoDB Light": {
        "url": "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
        "attribution": "© CartoDB"
    },
    "CartoDB Dark": {
        "url": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
        "attribution": "© CartoDB"
    },
    "Stamen Terrain": {
        "url": "https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png",
        "attribution": "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    }
}

# Define Bhuvan and other layers with proper configuration
BHUVAN_LAYERS = {
    # External (reliable) base layers
    "OpenStreetMap": {"type": "tile", "name": "OpenStreetMap"},
    "ESRI Satellite": {"type": "external_tile", "name": "ESRI Satellite"},
    "ESRI Terrain": {"type": "external_tile", "name": "ESRI Terrain"},
    "ESRI Topo": {"type": "external_tile", "name": "ESRI Topo"},
    "CartoDB Light": {"type": "external_tile", "name": "CartoDB Light"},
    "CartoDB Dark": {"type": "external_tile", "name": "CartoDB Dark"},
    "Stamen Terrain": {"type": "external_tile", "name": "Stamen Terrain"},
    
    # Bhuvan base layers - alternative formats
    "Bhuvan Basemap": {"type": "wms", "name": "sisdp_base:sisdp_basemap", "url": WMS_URL},
    "Bhuvan Satellite": {"type": "wms", "name": "BhuvanPDMC:BhuvanPDMC", "url": BHUVAN_RASTER_URL},
    "Bhuvan Terrain": {"type": "wms", "name": "organization:Elevation", "url": WMS_URL},
    
    # Overlay layers (multiple can be active)
    "Rivers": {"type": "wms", "name": "disaster:godavari_Rivers", "overlay": True, "url": WMS_URL},
    "State Boundaries": {"type": "wms", "name": "admin:INDIA_STATE", "overlay": True, "url": WMS_URL},
    "District Boundaries": {"type": "wms", "name": "admin:INDIA_DIST_250K", "overlay": True, "url": WMS_URL},
    "Roads": {"type": "wms", "name": "roads:ISAC_SHAR_v2", "overlay": True, "url": WMS_URL},
    "Railways": {"type": "wms", "name": "rail:all_india_rail", "overlay": True, "url": WMS_URL},
    "Geomorphology": {"type": "wms", "name": "geomorphology:GANGA_GEOM", "overlay": True, "url": WMS_URL},
    "LULC": {"type": "wms", "name": "lulc:GANGA_LULC", "overlay": True, "url": WMS_URL}
}

# Geocoding endpoints
BUHVAN_GEOCODE_URL = "http://bhuvan.nrsc.gov.in/search/placename"
OSM_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Unit conversion factors (from m²)
UNITS = {
    "km2": 1e-6,    # square metres → square kilometres
    "ha": 1e-4,     # square metres → hectares
    "m2": 1.0       # square metres
}

# Default active layers for initialization
DEFAULT_BASE_LAYER = "ESRI Satellite"  # More reliable default
DEFAULT_OVERLAYS = []  # No default overlays