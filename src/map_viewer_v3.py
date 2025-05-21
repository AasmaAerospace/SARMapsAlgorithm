# src/map_viewer_v3.py

from ipyleaflet import Map, WMSLayer, TileLayer, DrawControl, LayerGroup, basemaps
from src.config_v3 import WMS_URL, WMS_VERSION, DEFAULT_CENTER, DEFAULT_ZOOM, EXTERNAL_BASEMAPS
import time

class MapViewer:
    def __init__(self, center=DEFAULT_CENTER, zoom=DEFAULT_ZOOM, layers=None):
        # Initialize the map
        self.map = Map(center=center, zoom=zoom)
        
        # Track layers for management
        self._base_layer = None
        self._overlay_layers = {}  # Use dict to track by name
        
        # Add a default layer if no layers specified
        if not layers:
            self.add_tile_layer()
        else:
            self.add_wms_layer(layers)

        # Attach draw control (polygons & rectangles only)
        self.draw_control = self._make_draw_control()
        self.map.add_control(self.draw_control)

    def _make_draw_control(self):
        """Create a draw control with polygons and rectangles enabled"""
        dc = DrawControl(
            polygon={"shapeOptions": {"color": "#6bc2e5", "fillOpacity": 0.1}},
            rectangle={"shapeOptions": {"color": "#fca45d", "fillOpacity": 0.1}},
        )
        # Disable everything else
        dc.circle = {}
        dc.circlemarker = {}
        dc.polyline = {}
        dc.marker = {}
        return dc

    def add_tile_layer(self, tile_url=None, attribution="© OpenStreetMap contributors"):
        """Add a standard tile layer (like OpenStreetMap)"""
        # Remove old base layer if it exists
        if self._base_layer:
            self.map.remove_layer(self._base_layer)
        
        # Use provided URL or default to OpenStreetMap
        if not tile_url:
            tile_url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        
        # Create new tile layer
        self._base_layer = TileLayer(
            url=tile_url,
            attribution=attribution,
            max_zoom=19,
            max_native_zoom=18,
            min_zoom=2
        )
            
        self.map.add_layer(self._base_layer)
        return self._base_layer

    def add_external_tile_layer(self, basemap_name):
        """Add an external tile layer from the EXTERNAL_BASEMAPS configuration"""
        if basemap_name in EXTERNAL_BASEMAPS:
            basemap = EXTERNAL_BASEMAPS[basemap_name]
            return self.add_tile_layer(basemap["url"], basemap["attribution"])
        else:
            print(f"Warning: External basemap '{basemap_name}' not found.")
            return self.add_tile_layer()  # Fallback to default OSM

    def add_wms_layer(self, layer_name, is_base=True, layer_id=None, wms_url=None, wms_version=None):
        """
        Add a WMS layer to the map
        
        Parameters:
        -----------
        layer_name : str
            Layer name(s) to add
        is_base : bool
            Whether this is a base layer (True) or overlay (False)
        layer_id : str
            Identifier for the layer (for overlays)
        wms_url : str
            Optional custom WMS URL to use instead of the default
        wms_version : str
            Optional custom WMS version to use
        """
        # Use provided URL/version or defaults
        url = wms_url if wms_url else WMS_URL
        version = wms_version if wms_version else WMS_VERSION
        
        # Create WMS layer with better error handling
        try:
            # Parameters for WMS request
            wms_params = {
                'url': url,
                'layers': layer_name,
                'version': version,
                'format': 'image/png',
                'transparent': not is_base,  # Base layers shouldn't be transparent
                'attribution': 'ISRO Bhuvan',
                'crs': "EPSG:3857",  # Web Mercator projection
                'uppercase': True,    # Make parameter names uppercase (some WMS servers require this)
                'service': 'WMS'
            }
            
            # Create the WMS layer
            wms_layer = WMSLayer(**wms_params)
            
            # If this is a base layer, remove the old one
            if is_base:
                if self._base_layer:
                    self.map.remove_layer(self._base_layer)
                self._base_layer = wms_layer
            else:
                # For overlays, track by ID
                if layer_id:
                    # Remove existing layer with same ID if it exists
                    if layer_id in self._overlay_layers:
                        self.map.remove_layer(self._overlay_layers[layer_id])
                    # Add to overlay tracking dict
                    self._overlay_layers[layer_id] = wms_layer
            
            # Add to map
            self.map.add_layer(wms_layer)
            
            # Slight delay to let the layer load
            time.sleep(0.5)
            
            return wms_layer
            
        except Exception as e:
            print(f"Error adding WMS layer '{layer_name}': {e}")
            # Fall back to OpenStreetMap if there's an error with a base layer
            if is_base:
                print("Falling back to OpenStreetMap...")
                return self.add_tile_layer()
            return None

    def remove_overlay(self, layer_id):
        """Remove a specific overlay by ID"""
        if layer_id in self._overlay_layers:
            self.map.remove_layer(self._overlay_layers[layer_id])
            del self._overlay_layers[layer_id]

    def clear_all_overlays(self):
        """Remove all overlay layers"""
        for layer_id, layer in list(self._overlay_layers.items()):
            self.map.remove_layer(layer)
        self._overlay_layers = {}

    def clear_all_layers(self):
        """Remove all layers (base and overlays)"""
        # Remove base layer
        if self._base_layer:
            self.map.remove_layer(self._base_layer)
            self._base_layer = None
        
        # Remove all overlay layers
        self.clear_all_overlays()

    def get_map(self):
        """Get the ipyleaflet Map object"""
        return self.map

    def on_draw(self, handler):
        """
        Set handler for the DrawControl's on_draw event.
        handler signature should be: (target, action, geo_json)
        """
        self.draw_control.on_draw(handler)