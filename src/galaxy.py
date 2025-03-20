# src/galaxy.py

import pygame
import random
from src.solar_system import SolarSystem

class Galaxy:
    def __init__(self, galaxy_size=10000, num_stars=1000):
        self.galaxy_size = galaxy_size
        self.num_stars = num_stars
        self.stars = self._generate_stars(num_stars, galaxy_size)
        self.solar_systems = self._generate_solar_systems()

    def _generate_stars(self, num_stars, galaxy_size):
        """Generate stars with random positions and attributes."""
        star_colors = [(255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]  # Star colors
        stars = []

        for i in range(num_stars):
            x = random.randint(0, galaxy_size)  # Random x-coordinate
            y = random.randint(0, galaxy_size)  # Random y-coordinate
            radius = random.randint(5, 15)  # Random size for stars
            color = random.choice(star_colors)  # Random color
            name = f"Star {i + 1}"  # Unique name for each star

            stars.append({
                "name": name,
                "x": x,
                "y": y,
                "radius": radius,
                "color": color
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
    
    def get_solar_systems(self, star_name):
        #access each one from the dictionary of stars
        return self.solar_systems.get(star_name)

    def update(self, time_delta): 
        #add logic for backgound events or anything that isn't pefectly static, such as sovereignty map
        pass
