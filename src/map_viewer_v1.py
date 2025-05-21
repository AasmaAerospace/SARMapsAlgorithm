# src/map_viewer.py

from ipyleaflet import Map, WMSLayer, DrawControl
from src.config_v1 import (
    WMS_URL,
    WMS_VERSION,
    DEFAULT_LAYERS,
    DEFAULT_CENTER,
    DEFAULT_ZOOM
)

class MapViewer:
    """
    A thin wrapper around ipyleaflet.Map that:
      - adds an ISRO Bhuvan WMS basemap
      - attaches only polygon & rectangle draw tools
      - exposes on_draw() to hook your callback
    """
    def __init__(
        self,
        center=DEFAULT_CENTER,
        zoom=DEFAULT_ZOOM,
        layers=DEFAULT_LAYERS
    ):
        # create the map widget
        self.map = Map(center=center, zoom=zoom)

        # add the WMS layer
        self._add_wms_layer(layers)

        # add the draw control (only polygon & rectangle)
        self.draw_control = self._add_draw_control()

    def _add_wms_layer(self, layers):
        # allow either a single string or a list of layer names
        if isinstance(layers, (list, tuple)):
            layers_str = ",".join(layers)
        else:
            layers_str = layers

        wms = WMSLayer(
            url=WMS_URL,
            layers=layers_str,
            version=WMS_VERSION,
            format='image/png',
            transparent=True,
            attribution='ISRO Bhuvan'
        )
        self.map.add_layer(wms)

    def _add_draw_control(self):
        dc = DrawControl()

        # enable only polygon & rectangle, with your style
        dc.polygon = {
            "shapeOptions": {"color": "#6bc2e5", "fillOpacity": 0.1}
        }
        dc.rectangle = {
            "shapeOptions": {"color": "#fca45d", "fillOpacity": 0.1}
        }

        # disable everything else
        dc.circle = {}
        dc.circlemarker = {}
        dc.polyline = {}
        dc.marker = {}

        self.map.add_control(dc)
        return dc

    def get_map(self):
        """Return the underlying ipyleaflet.Map widget."""
        return self.map

    def on_draw(self, callback):
        """
        Hook your callback to the draw event.
        callback will be called as: callback(target, action, geo_json)
        """
        self.draw_control.on_draw(callback)
