# src/map_viewer_v4.py

from ipyleaflet import Map, WMSLayer, TileLayer, DrawControl, CircleMarker, Polygon, Polyline
from src.config_v4 import WMS_URL, WMS_VERSION, DEFAULT_CENTER, DEFAULT_ZOOM, EXTERNAL_BASEMAPS

class MapViewer:
    def __init__(self, center=DEFAULT_CENTER, zoom=DEFAULT_ZOOM, layers=None):
        """Initialize the map viewer with the specified center and zoom level"""
        # Initialize the map
        self.map = Map(center=center, zoom=zoom)
        
        # Track layers
        self._base_layer = None
        self._overlay_layers = {}
        self._simulation_layers = []
        
        # Current drawn shape
        self.current_polygon = None
        
        # Add default layer if specified
        if layers:
            self.add_wms_layer(layers)
        else:
            self.add_tile_layer()

        # Attach draw control
        self.draw_control = self._make_draw_control()
        self.map.add_control(self.draw_control)

    def _make_draw_control(self):
        """Create a draw control with polygons and rectangles enabled"""
        dc = DrawControl(
            polygon={"shapeOptions": {"color": "#6bc2e5", "fillOpacity": 0.1}},
            rectangle={"shapeOptions": {"color": "#fca45d", "fillOpacity": 0.1}},
        )
        # Disable other drawing tools
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
        """Add a WMS layer to the map"""
        # Use provided URL/version or defaults
        url = wms_url if wms_url else WMS_URL
        version = wms_version if wms_version else WMS_VERSION
        
        try:
            # Create WMS layer
            wms_layer = WMSLayer(
                url=url,
                layers=layer_name,
                version=version,
                format='image/png',
                transparent=not is_base,
                attribution='ISRO Bhuvan'
            )
            
            # Handle base vs overlay
            if is_base:
                if self._base_layer:
                    self.map.remove_layer(self._base_layer)
                self._base_layer = wms_layer
            else:
                if layer_id:
                    if layer_id in self._overlay_layers:
                        self.map.remove_layer(self._overlay_layers[layer_id])
                    self._overlay_layers[layer_id] = wms_layer
            
            # Add to map
            self.map.add_layer(wms_layer)
            return wms_layer
            
        except Exception as e:
            print(f"Error adding WMS layer '{layer_name}': {e}")
            if is_base:
                print("Falling back to OpenStreetMap...")
                return self.add_tile_layer()
            return None

    def add_polygon(self, coords, color="#6bc2e5", fill_opacity=0.1):
        """Add a polygon to the map"""
        polygon = Polygon(
            locations=coords,
            color=color,
            fill_opacity=fill_opacity,
            weight=2
        )
        self.map.add_layer(polygon)
        self.current_polygon = polygon
        return polygon
        
    def add_drone_marker(self, position, color="blue", radius=5):
        """Add a drone marker at the specified position"""
        marker = CircleMarker(
            location=position,
            radius=radius,
            color=color,
            fill_color=color,
            fill_opacity=0.8,
            weight=2
        )
        self.map.add_layer(marker)
        self._simulation_layers.append(marker)
        return marker
        
    def add_drone_path(self, path, color="blue", weight=2, opacity=0.7):
        """Add a path line for a drone's movement history"""
        # Need at least 2 points for a path
        if len(path) < 2:
            return None
            
        path_line = Polyline(
            locations=path,
            color=color,
            weight=weight,
            opacity=opacity
        )
        self.map.add_layer(path_line)
        self._simulation_layers.append(path_line)
        return path_line
        
    def clear_simulation_layers(self):
        """Remove all simulation-related layers (drones, paths)"""
        for layer in self._simulation_layers:
            self.map.remove_layer(layer)
        self._simulation_layers = []
        
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
        if self._base_layer:
            self.map.remove_layer(self._base_layer)
            self._base_layer = None
        self.clear_all_overlays()

    def get_map(self):
        """Get the ipyleaflet Map object"""
        return self.map

    def on_draw(self, handler):
        """Set handler for the DrawControl's on_draw event"""
        self.draw_control.on_draw(handler)