# src/utils/map_utils.py

def update_map_layers(map_viewer, active_base, active_overlays, bhuvan_layers, status_callback=None):
    """
    Update all map layers based on current selections
    
    Parameters:
    -----------
    map_viewer : MapViewer
        The map viewer instance
    active_base : str
        The name of the active base layer
    active_overlays : list or set
        Names of active overlay layers
    bhuvan_layers : dict
        Configuration dict of available layers
    status_callback : function, optional
        Function to call with status updates
    """
    # Helper function for status updates
    def update_status(message):
        if status_callback:
            status_callback(message)
        else:
            print(message)
    
    # Clear existing layers
    map_viewer.clear_all_layers()
    
    # Add the selected base layer
    base_layer_info = bhuvan_layers[active_base]
    
    if base_layer_info["type"] == "wms":
        custom_url = base_layer_info.get("url", None)
        update_status(f"Loading WMS layer: {base_layer_info['name']}...")
        result = map_viewer.add_wms_layer(base_layer_info["name"], is_base=True, wms_url=custom_url)
        if result is None:
            update_status("WMS layer failed to load. Falling back to OpenStreetMap...")
            map_viewer.add_tile_layer()
    elif base_layer_info["type"] == "external_tile":
        update_status(f"Loading external tile layer: {active_base}...")
        map_viewer.add_external_tile_layer(active_base)
    else:  # Default tile layer
        update_status("Loading OSM tile layer...")
        map_viewer.add_tile_layer()
    
    # Add all active overlays
    for overlay_name in active_overlays:
        overlay_info = bhuvan_layers[overlay_name]
        if overlay_info["type"] == "wms":
            custom_url = overlay_info.get("url", None)
            update_status(f"Adding overlay: {overlay_name}...")
            result = map_viewer.add_wms_layer(
                overlay_info["name"], 
                is_base=False, 
                layer_id=overlay_name, 
                wms_url=custom_url
            )
            if result is None:
                update_status(f"Failed to add overlay: {overlay_name}")