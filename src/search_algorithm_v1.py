# src/search_algorithm_v4.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.path as mpath
from matplotlib.collections import LineCollection
import random
import math
from scipy.ndimage import gaussian_filter
from IPython.display import clear_output

class DroneSearchSimulation:
    def __init__(self, area_coords, n_drones=5, boundary_padding=10):
        """
        Initialize the drone search simulation
        
        Parameters:
        -----------
        area_coords : list of (lon, lat) tuples
            The coordinates of the polygon defining the search area
        n_drones : int
            Number of drones to use in the simulation
        boundary_padding : int
            Padding distance from the boundary
        """
        self.area_coords = area_coords
        self.n_drones = n_drones
        self.boundary_padding = boundary_padding
        
        # Extract min/max coordinates for conversion
        self.min_x = min(coord[0] for coord in area_coords)
        self.min_y = min(coord[1] for coord in area_coords)
        self.max_x = max(coord[0] for coord in area_coords)
        self.max_y = max(coord[1] for coord in area_coords)
        
        # Calculate grid size based on the area
        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y
        self.grid_size = max(self.width, self.height)
        
        # Internal parameters
        self.drone_radius = 5
        self.scan_radius = 2 * self.drone_radius
        
        # Setup grid for coverage tracking
        self.grid_resolution = 50
        self.exploration_grid = np.zeros((self.grid_resolution, self.grid_resolution))
        
        # Initialize drone positions at a starting point (e.g., first point of polygon)
        self.start_point = self.convert_coords_to_grid(self.area_coords[0])
        self.drone_positions = []
        for i in range(self.n_drones):
            # Spread drones slightly at the starting point
            x = self.start_point[0] + np.random.randint(-10, 10)
            y = self.start_point[1] + np.random.randint(-10, 10)
            x = max(self.boundary_padding, min(self.grid_size - self.boundary_padding, x))
            y = max(self.boundary_padding, min(self.grid_size - self.boundary_padding, y))
            self.drone_positions.append([x, y])
        
        # Initialize drone path history and velocities
        self.drone_paths = [[] for _ in range(self.n_drones)]
        self.drone_velocities = []
        self.drone_targets = []
        
        for _ in range(self.n_drones):
            angle = 2 * np.pi * np.random.random()
            speed = 2 + np.random.random() * 2
            vx = speed * np.cos(angle)
            vy = speed * np.sin(angle)
            self.drone_velocities.append([vx, vy])
            self.drone_targets.append(None)
        
        # Create polygon path for point-in-polygon testing
        self.area_path = mpath.Path(self.convert_polygon_to_grid(self.area_coords))
    
    def convert_coords_to_grid(self, coord):
        """Convert a real-world coordinate to a grid coordinate"""
        # Scale to grid size
        grid_x = ((coord[0] - self.min_x) / self.width) * self.grid_size
        grid_y = ((coord[1] - self.min_y) / self.height) * self.grid_size
        return [grid_x, grid_y]
    
    def convert_polygon_to_grid(self, coords_list):
        """Convert all polygon coordinates to grid coordinates"""
        return [self.convert_coords_to_grid(coord) for coord in coords_list]
    
    def convert_grid_to_coords(self, grid_point):
        """Convert a grid coordinate back to a real-world coordinate"""
        # Scale from grid size back to real-world coordinates
        real_x = self.min_x + (grid_point[0] / self.grid_size) * self.width
        real_y = self.min_y + (grid_point[1] / self.grid_size) * self.height
        return [real_x, real_y]
        
    def is_point_inside_area(self, point):
        """Check if a point is inside the defined search area"""
        return self.area_path.contains_point(point)
    
    def get_exploration_score(self, x, y):
        """Calculate exploration score for a point (lower is better)"""
        # Convert position to grid index
        grid_x = int(x / self.grid_size * self.grid_resolution)
        grid_x = max(0, min(self.grid_resolution-1, grid_x))
        grid_y = int(y / self.grid_size * self.grid_resolution)
        grid_y = max(0, min(self.grid_resolution-1, grid_y))
        
        # Calculate score based on unexplored areas
        score = 1.0 - self.exploration_grid[grid_y, grid_x]
        return score
    
    def get_new_target(self, drone_id, current_pos):
        """Find a new target position for a drone"""
        # Get least explored regions
        flat_indices = np.argsort(self.exploration_grid.flatten())
        least_explored = flat_indices[:20]  # Get top 20 least explored cells
        
        # Convert to 2D indices
        candidates = []
        for idx in least_explored:
            y_idx = idx // self.grid_resolution
            x_idx = idx % self.grid_resolution
            # Convert to actual coordinates
            x = (x_idx + 0.5) * self.grid_size / self.grid_resolution
            y = (y_idx + 0.5) * self.grid_size / self.grid_resolution
            
            # Check if inside search area
            if self.is_point_inside_area([x, y]):
                candidates.append((x, y))
        
        if candidates:
            # Get random one from candidates
            return random.choice(candidates)
        else:
            # Random position within search area if no good candidates
            max_attempts = 50
            attempts = 0
            while attempts < max_attempts:
                x = np.random.randint(self.boundary_padding, self.grid_size - self.boundary_padding)
                y = np.random.randint(self.boundary_padding, self.grid_size - self.boundary_padding)
                if self.is_point_inside_area([x, y]):
                    return (x, y)
                attempts += 1
            
            # If all attempts fail, return current position
            return current_pos
    
    def update_grid(self):
        """Update the exploration grid based on drone positions"""
        for x, y in self.drone_positions:
            # Define scan area radius in grid cells
            scan_cell_radius = int(self.scan_radius * 5 / self.grid_size * self.grid_resolution)
            
            # Get center cell coordinates
            grid_x = int(x / self.grid_size * self.grid_resolution)
            grid_x = max(0, min(self.grid_resolution-1, grid_x))
            grid_y = int(y / self.grid_size * self.grid_resolution)
            grid_y = max(0, min(self.grid_resolution-1, grid_y))
            
            # Update cells within scan radius
            for dx in range(-scan_cell_radius, scan_cell_radius + 1):
                for dy in range(-scan_cell_radius, scan_cell_radius + 1):
                    nx = grid_x + dx
                    ny = grid_y + dy
                    # Check if within grid bounds and within scan circle
                    if (0 <= nx < self.grid_resolution and 0 <= ny < self.grid_resolution and
                        dx*dx + dy*dy <= scan_cell_radius*scan_cell_radius):
                        
                        # Check if point is inside search area
                        point_x = (nx + 0.5) * self.grid_size / self.grid_resolution
                        point_y = (ny + 0.5) * self.grid_size / self.grid_resolution
                        
                        if self.is_point_inside_area([point_x, point_y]):
                            # Apply diminishing effect based on distance
                            dist = np.sqrt(dx*dx + dy*dy) / scan_cell_radius
                            effect = 0.2 * max(0, 1 - dist)
                            self.exploration_grid[ny, nx] = min(1.0, self.exploration_grid[ny, nx] + effect)
    
    def simulate_step(self):
        """Simulate one step of the drone movement"""
        # Update drone positions
        for i in range(self.n_drones):
            # Get or update target
            if self.drone_targets[i] is None or np.random.random() < 0.01:
                self.drone_targets[i] = self.get_new_target(i, self.drone_positions[i])
            
            target_x, target_y = self.drone_targets[i]
            current_x, current_y = self.drone_positions[i]
            
            # Calculate direction to target
            dx = target_x - current_x
            dy = target_y - current_y
            distance = np.sqrt(dx*dx + dy*dy)
            
            if distance < 5:  # If close to target, get new target
                self.drone_targets[i] = self.get_new_target(i, self.drone_positions[i])
            else:
                # Normalize and scale
                dx /= distance
                dy /= distance
                speed = 2 + np.random.random() * 2
                self.drone_velocities[i] = [dx * speed, dy * speed]
            
            # Apply velocity
            vx, vy = self.drone_velocities[i]
            new_x = current_x + vx
            new_y = current_y + vy
            
            # Boundary check and ensure inside search area
            if not self.is_point_inside_area([new_x, new_y]):
                # Bounce off boundary
                self.drone_velocities[i][0] *= -1
                self.drone_velocities[i][1] *= -1
                
                # Update with reversed velocity
                vx, vy = self.drone_velocities[i]
                new_x = current_x + vx
                new_y = current_y + vy
                
                # If still outside, move back towards center
                if not self.is_point_inside_area([new_x, new_y]):
                    center_x = sum(p[0] for p in self.convert_polygon_to_grid(self.area_coords)) / len(self.area_coords)
                    center_y = sum(p[1] for p in self.convert_polygon_to_grid(self.area_coords)) / len(self.area_coords)
                    
                    dx = center_x - current_x
                    dy = center_y - current_y
                    distance = np.sqrt(dx*dx + dy*dy)
                    
                    # Normalize and scale
                    if distance > 0:
                        dx /= distance
                        dy /= distance
                        speed = 2
                        self.drone_velocities[i] = [dx * speed, dy * speed]
                        vx, vy = self.drone_velocities[i]
                        new_x = current_x + vx
                        new_y = current_y + vy
            
            # Update position
            self.drone_positions[i] = [new_x, new_y]
            
            # Store path
            self.drone_paths[i].append((new_x, new_y))
            if len(self.drone_paths[i]) > 50:  # Keep only last 50 positions
                self.drone_paths[i].pop(0)
        
        # Update exploration grid
        self.update_grid()
        
        # Calculate coverage
        covered_cells = np.sum(self.exploration_grid > 0.2)  # Threshold for "covered"
        total_explorable_cells = self.get_explorable_cells_count()
        coverage_percent = (covered_cells / total_explorable_cells) * 100 if total_explorable_cells > 0 else 0
        
        return {
            'drone_positions': self.drone_positions.copy(),
            'drone_paths': [path.copy() for path in self.drone_paths],
            'exploration_grid': self.exploration_grid.copy(),
            'coverage_percent': coverage_percent
        }
    
    def get_explorable_cells_count(self):
        """Count the number of grid cells that are inside the search area"""
        count = 0
        for y in range(self.grid_resolution):
            for x in range(self.grid_resolution):
                # Convert to grid coordinates
                point_x = (x + 0.5) * self.grid_size / self.grid_resolution
                point_y = (y + 0.5) * self.grid_size / self.grid_resolution
                
                if self.is_point_inside_area([point_x, point_y]):
                    count += 1
        return count
    
    def get_real_world_paths(self):
        """Convert grid paths to real-world coordinates"""
        real_paths = []
        for path in self.drone_paths:
            real_path = [self.convert_grid_to_coords(point) for point in path]
            real_paths.append(real_path)
        return real_paths
    
    def get_real_world_positions(self):
        """Convert grid positions to real-world coordinates"""
        return [self.convert_grid_to_coords(pos) for pos in self.drone_positions]