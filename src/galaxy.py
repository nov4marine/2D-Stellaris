# src/galaxy.py

import pygame
import random
import math
from src.solar_system import SolarSystem

class Galaxy:
    def __init__(self, galaxy_size=8000, num_stars=1000):
        self.galaxy_size = galaxy_size
        self.num_stars = num_stars
        self.stars = self._generate_stars(num_stars, galaxy_size)
        self.solar_systems = self._generate_solar_systems()
        self.hyperlanes = self._generate_hyperlanes()

    def _generate_stars(self, num_stars, galaxy_size):
        """Generate stars with random positions and attributes in a galaxy shape."""
        star_colors = [(255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
        stars = []

        num_arms = 4  # Number of spiral arms
        arm_tightness = 0.4  # Controls arm winding
        arm_spread = 0.05  # Spread around arms
        center_radius = galaxy_size * 0.1  # Minimum radius for the empty core
        overall_rotation = math.pi / 4  # Rotate the entire galaxy
        min_distance = 100  # Minimum distance between stars

        for i in range(num_stars):
            while True:
                # Radial distance (ensuring it's outside the empty center)
                r = random.uniform(center_radius, galaxy_size)

                # Angle for the spiral arms
                arm_index = i % num_arms
                arm_angle = arm_index * (2 * math.pi / num_arms)

                theta = overall_rotation + arm_angle + arm_tightness * r

                # Convert polar to Cartesian with tighter spread
                x = r * math.cos(theta) + random.uniform(-arm_spread * r, arm_spread * r)
                y = r * math.sin(theta) + random.uniform(-arm_spread * r, arm_spread * r)

                # Check minimum distance to other stars
                too_close = False
                for star in stars:
                    distance = math.sqrt((x - star['x']) ** 2 + (y - star['y']) ** 2)
                    if distance < min_distance:
                        too_close = True
                        break

                # Add the star only if it's far enough from others
                if not too_close:
                    break

            # Assign random attributes to the star
            radius = random.randint(10, 15)
            color = random.choice(star_colors)
            name = f"star {i + 1}"

            # Create a dictionary for the star's attributes
            stars.append({
                "name": name,
                "x": x,
                "y": y,
                "radius": radius,
                "color": color,
            })

        return stars
    
    def _generate_solar_systems(self):
        """simulate a solar system instance for each star in the galaxy"""
        solar_systems = {}
        for star in self.stars:
            #use the star's name as the key and instance a solar system
            solar_systems[star["name"]] = SolarSystem(star_name=star["name"], star_type="main sequence")
        return solar_systems
    
    def update_solar_systems(self, time_delta):
        """update solar systems"""
        for solar_system in self.solar_systems.values():
            solar_system.update(time_delta)
    
    def render_galaxy(self, screen, camera):
        """render the galaxy"""
        for star in self.stars:
            #convert world coordinates to screen coordinates using the camera
            screen_x, screen_y = camera.apply(star["x"], star["y"])
            #draw star as a circle
            pygame.draw.circle(screen, star["color"], (int(screen_x), int(screen_y)), int(star["radius"] * camera.zoom))
            # Dynamically update the star's rect for collision detection
            star["rect"] = pygame.Rect(
                int(screen_x - star["radius"] * camera.zoom),
                int(screen_y - star["radius"] * camera.zoom),
                int(star["radius"] * 2 * camera.zoom),
                int(star["radius"] * 2 * camera.zoom)
            )
        
        #Draw faint hyperlanes between connected stars.
        for line in self.hyperlanes:
            start_x, start_y = camera.apply(line[0][0], line[0][1])
            end_x, end_y = camera.apply(line[1][0], line[1][1])
            pygame.draw.line(screen, (255, 255, 255, 50), (start_x, start_y), (end_x, end_y), 1)
    
    def _generate_hyperlanes(self, max_distance=300):
        """Generate hyperlane connections between nearby stars."""
        hyperlanes = []  # Stores line coordinates
        
        for star in self.stars:
            star_x, star_y = star["x"], star["y"]
            
            for other_star in self.stars:
                if star == other_star:
                    continue  # Skip self-connections
                
                other_x, other_y = other_star["x"], other_star["y"]
                
                # Compute distance
                distance = math.sqrt((star_x - other_x)**2 + (star_y - other_y)**2)
                
                if distance <= max_distance:  # ✅ If close enough, create a hyperlane
                    hyperlanes.append(((star_x, star_y), (other_x, other_y)))

        return hyperlanes

    def get_solar_systems(self, star_name):
        #access each one from the dictionary of stars
        return self.solar_systems.get(star_name)

    def update(self, time_delta): 
        #add logic for backgound events or anything that isn't pefectly static, such as sovereignty map
        pass
