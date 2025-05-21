# src/config.py

# ISRO Bhuvan OGC WMS settings
WMS_URL = "https://bhuvan-vec2.nrsc.gov.in/bhuvan/wms"       # Bhuvan Web Map Service endpoint :contentReference[oaicite:0]{index=0}
WMS_VERSION   = "1.3.0"
#WMS_VERSION = "1.1.1"                                        # Supported WMS version :contentReference[oaicite:1]{index=1}
#DEFAULT_LAYERS = ["lulc:BR_LULC50K_1112"]                    # Default LULC 50K layer :contentReference[oaicite:2]{index=2}

#DEFAULT_LAYERS = ["sisdp_base:sisdp_basemap"]   # full-extent Bhuvan base map

#BHUVAN_LAYERS = {
#    "Land-use (LULC)" : DEFAULT_LAYERS,
#    "Elevation (DEM)" : "organization:Elevation",
#    "Geomorphology"   : "geomorphology:GANGA_GEOM",
#    "Salinity"        : "salinity:GANGA_SAL",
    # …add more here as you discover them…
#}

# The default (base) layer we fall back to
DEFAULT_LAYER = "Basemap"

# A small, curated set of Bhuvan layers that are broadly useful
BHUVAN_LAYERS = {
    
    "Basemap":           "sisdp_base:sisdp_basemap", # the “classic” ISRO basemap                

    
    "Satellite":         "BhuvanPDMC:BhuvanPDMC", # high-resolution satellite imagery from the PDMC service                   

    
    "Terrain (Elevation)": "organization:Elevation", # shaded relief / hill-shade (terrain)                

    
    "Geomorphology":     "geomorphology:GANGA_GEOM", # broad-scale landform/rock type patterns                

    
    "LULC":              "lulc:GANGA_LULC", # land-use / land-cover                       

    
    "Roads":             "roads:ISAC_SHAR_v2", # major roads                     

    
    "Admin Boundaries":  "admin:INDIA_STATE", # state-level administrative boundaries                      

    
    "Salinity":          "salinity:GANGA_SAL", # soil / groundwater salinity patterns                    

    
    "Lineaments":        "lineament:GANGA_LN", # structural lineaments
}


DEFAULT_CENTER = (20.5937, 78.9629)                          # Approximate geographic centre of India
DEFAULT_ZOOM = 5                                             # Initial zoom level

# Geocoding endpoints
BUHVAN_GEOCODE_URL = "http://bhuvan.nrsc.gov.in/search/placename"  # Bhuvan place-lookup API :contentReference[oaicite:3]{index=3}
OSM_NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"   # Fallback if needed

# Unit conversion factors (from m²)
UNITS = {
    "km2": 1e-6,    # square metres → square kilometres
    "ha": 1e-4,     # square metres → hectares
    "m2": 1.0       # square metres
}
