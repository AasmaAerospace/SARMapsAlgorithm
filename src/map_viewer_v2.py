# src/map_viewer_v2.py

from ipyleaflet import Map, WMSLayer, DrawControl
from src.config_v2    import WMS_URL, WMS_VERSION, DEFAULT_CENTER, DEFAULT_ZOOM

class MapViewer:
    def __init__(self, center=DEFAULT_CENTER, zoom=DEFAULT_ZOOM, layers=None):
        # 1) make the map
        self.map = Map(center=center, zoom=zoom)
        self._wms_layer = None

        # 2) add an initial Bhuvan overlay if requested
        if layers:
            self.add_wms_layer(layers)

        # 3) attach draw control (polygons & rectangles only)
        self.draw_control = self._make_draw_control()
        self.map.add_control(self.draw_control)

    def _make_draw_control(self):
        dc = DrawControl(
            polygon   = {"shapeOptions": {"color": "#6bc2e5", "fillOpacity": 0.1}},
            rectangle = {"shapeOptions": {"color": "#fca45d", "fillOpacity": 0.1}},
        )
        # disable everything else by assigning empty dicts
        dc.circle       = {}
        dc.circlemarker = {}
        dc.polyline     = {}
        dc.marker       = {}
        return dc

    def add_wms_layer(self, layers):
        # remove old
        if self._wms_layer:
            self.map.remove_layer(self._wms_layer)

        # if they passed a list, join it
        if isinstance(layers, (list, tuple)):
            layer_param = ",".join(layers)
        else:
            layer_param = layers

        self._wms_layer = WMSLayer(
            url         = WMS_URL,
            layers      = layer_param,
            version     = WMS_VERSION,
            format      = 'image/png',
            transparent = True,
            attribution = 'ISRO Bhuvan'
        )
        self.map.add_layer(self._wms_layer)
        return self._wms_layer

    def get_map(self):
        return self.map

    def on_draw(self, handler):
        """
        Proxy for the DrawControl’s on_draw event.
        handler signature should be: (target, action, geo_json)
        """
        self.draw_control.on_draw(handler)
