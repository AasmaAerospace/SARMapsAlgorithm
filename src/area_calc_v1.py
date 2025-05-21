# src/area_calc.py

from shapely.geometry import Polygon
from pyproj import Transformer
from src.config_v1 import UNITS

def compute_area(polygon_coords, unit: str = "km2") -> float:
    """
    Compute the area of a polygon defined by a list of (lon, lat) tuples.

    Parameters
    ----------
    polygon_coords : List[Tuple[float, float]]
        The vertices of the polygon in (longitude, latitude) order.
    unit : str, optional
        The desired output unit: one of UNITS keys ("km2", "ha", "m2").
        Defaults to "km2".

    Returns
    -------
    float
        The area of the polygon in the specified unit.

    Raises
    ------
    ValueError
        If an unsupported unit is requested.
    """
    # 1. Build the Shapely polygon in geographic coordinates
    geo_poly = Polygon(polygon_coords)
    if not geo_poly.is_valid:
        geo_poly = geo_poly.buffer(0)

    # 2. Project to an equal-area CRS (World Mollweide: ESRI:54009)
    transformer = Transformer.from_crs("EPSG:4326", "ESRI:54009", always_xy=True)
    projected_coords = [transformer.transform(lon, lat) for lon, lat in polygon_coords]
    proj_poly = Polygon(projected_coords)

    # 3. Compute area in square metres
    area_m2 = proj_poly.area

    # 4. Convert to requested unit
    try:
        factor = UNITS[unit]
    except KeyError:
        raise ValueError(f"Unsupported unit '{unit}'. Choose from {list(UNITS.keys())}")
    return area_m2 * factor
