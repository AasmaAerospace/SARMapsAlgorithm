# src/utils/simulation_utils.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io
import base64
from IPython.display import HTML, display, clear_output

def create_coverage_visualization(exploration_grid):
    """Create a visualization of the exploration grid as a base64 PNG"""
    # Create a figure
    fig, ax = plt.subplots(figsize=(4, 4))
    
    # Create a custom colormap (greens with transparency)
    colors = [(0, 0, 0, 0), (0.2, 0.8, 0.2, 0.6)]
    cmap = LinearSegmentedColormap.from_list('coverage', colors)
    
    # Plot the exploration grid
    im = ax.imshow(exploration_grid, cmap=cmap, interpolation='bilinear')
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)
        
    # Save to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)
    
    # Encode as base64
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return img_str

def display_coverage_progression(visualizations):
    """Display a series of coverage visualizations"""
    html_parts = ["<div style='display:flex; flex-wrap:wrap; justify-content:center;'>"]
    
    for viz in visualizations:
        html_parts.append(
            f"<div style='display:inline-block; margin:10px; text-align:center;'>"
            f"<p>Step {viz['step']}<br>Coverage: {viz['coverage']:.1f}%</p>"
            f"<img src='data:image/png;base64,{viz['img']}' style='width:150px; border:1px solid #ddd'/>"
            f"</div>"
        )
    
    html_parts.append("</div>")
    return HTML("".join(html_parts))

def run_simulation(simulation, max_steps, viz_steps, progress_callback=None, status_callback=None):
    """
    Run a simulation for the specified number of steps
    
    Parameters:
    -----------
    simulation : DroneSearchSimulation
        The simulation instance
    max_steps : int
        Maximum number of steps to run
    viz_steps : list
        Steps at which to save visualizations
    progress_callback : function, optional
        Function to call with progress updates (0-100)
    status_callback : function, optional
        Function to call with status updates
    
    Returns:
    --------
    dict
        A dictionary containing simulation results
    """
    # Helper functions for updates
    def update_progress(value):
        if progress_callback:
            progress_callback(value)
    
    def update_status(message):
        if status_callback:
            status_callback(message)
        else:
            print(message)
    
    update_status("Starting simulation...")
    
    # Store visualizations
    visualizations = []
    
    # Run simulation steps
    for step in range(max_steps):
        # Simulate one step
        result = simulation.simulate_step()
        
        # Update progress (0-100%)
        progress_percent = (step + 1) / max_steps * 100
        update_progress(progress_percent)
        
        # Save visualization at specific steps
        if step in viz_steps:
            img = create_coverage_visualization(result['exploration_grid'])
            visualizations.append({
                'step': step,
                'coverage': result['coverage_percent'],
                'img': img
            })
    
    update_status(f"Simulation complete! {max_steps} steps processed.")
    update_status(f"Final coverage: {result['coverage_percent']:.1f}%")
    
    # Return final result and visualizations
    return {
        'final_result': result,
        'visualizations': visualizations,
        'drone_positions': simulation.get_real_world_positions(),
        'drone_paths': simulation.get_real_world_paths()
    }