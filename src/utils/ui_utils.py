# src/utils/ui_utils.py

import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

def create_search_ui(drone_count_default=5, drone_count_max=10):
    """Create UI elements for search"""
    # Search simulation controls
    drone_count = widgets.IntSlider(
        value=drone_count_default,
        min=1,
        max=drone_count_max,
        step=1,
        description='Drones:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )

    start_search_btn = widgets.Button(
        description='Start Search',
        disabled=True,
        button_style='success',
        tooltip='Start drone search simulation in the selected area',
        icon='rocket'
    )

    stop_search_btn = widgets.Button(
        description='Stop Search',
        disabled=True,
        button_style='danger',
        tooltip='Stop the current simulation',
        icon='stop'
    )
    
    coverage_progress = widgets.FloatProgress(
        value=0,
        min=0,
        max=100,
        description='Coverage:',
        bar_style='info',
        orientation='horizontal'
    )
    
    # Hide progress bar initially
    coverage_progress.layout.visibility = 'hidden'
    
    # Output areas
    status_out = widgets.Output()
    area_out = widgets.Output()
    simulation_out = widgets.Output(layout={'border': '1px solid #ddd', 'padding': '10px', 'min_height': '100px'})
    
    return {
        'drone_count': drone_count,
        'start_search_btn': start_search_btn,
        'stop_search_btn': stop_search_btn,
        'coverage_progress': coverage_progress,
        'status_out': status_out,
        'area_out': area_out,
        'simulation_out': simulation_out
    }

def create_map_ui(bhuvan_layers, default_base_layer="ESRI Satellite"):
    """Create UI elements for map controls"""
    # Base layer selector
    base_selector = widgets.Dropdown(
        options=[k for k, v in bhuvan_layers.items() if not v.get('overlay', False)],
        value=default_base_layer,
        description='Base layer:'
    )

    # Overlay selectors
    overlay_checkboxes = {}
    for layer_name, layer_info in bhuvan_layers.items():
        if layer_info.get('overlay', False):
            checkbox = widgets.Checkbox(
                value=False,
                description=layer_name,
                disabled=False
            )
            overlay_checkboxes[layer_name] = checkbox

    overlay_accordion = widgets.Accordion(
        children=[widgets.VBox([overlay_checkboxes[k] for k in overlay_checkboxes])],
        selected_index=None
    )
    overlay_accordion.set_title(0, 'Overlays')
    
    # Place search
    search_box = widgets.Text(description='Search:')
    search_btn = widgets.Button(description='Go')
    
    # Unit selector for area calculations
    unit_selector = widgets.Dropdown(
        options=[('km²', 'km2'), ('ha', 'ha'), ('m²', 'm2')],
        value='km2',
        description='Units:'
    )
    
    return {
        'base_selector': base_selector,
        'overlay_checkboxes': overlay_checkboxes,
        'overlay_accordion': overlay_accordion,
        'search_box': search_box,
        'search_btn': search_btn,
        'unit_selector': unit_selector
    }

def create_layout(map_ui, search_ui):
    """Create the main layout for the application"""
    # Search controls
    search_controls = widgets.HBox([map_ui['search_box'], map_ui['search_btn'], map_ui['unit_selector']])
    
    # Simulation controls
    simulation_controls = widgets.HBox([
        search_ui['drone_count'], 
        search_ui['start_search_btn'], 
        search_ui['stop_search_btn']
    ])
    
    # Layer controls
    layer_controls = widgets.VBox([map_ui['base_selector'], map_ui['overlay_accordion']])
    
    # Output area
    output_area = widgets.VBox([
        search_ui['coverage_progress'], 
        search_ui['simulation_out'], 
        search_ui['status_out'], 
        search_ui['area_out']
    ])
    
    # Main tabs
    main_tabs = widgets.Tab()
    main_tabs.children = [layer_controls, widgets.VBox([simulation_controls, output_area])]
    main_tabs.set_title(0, 'Map Layers')
    main_tabs.set_title(1, 'Search Simulation')
    
    return {
        'search_controls': search_controls,
        'main_tabs': main_tabs
    }