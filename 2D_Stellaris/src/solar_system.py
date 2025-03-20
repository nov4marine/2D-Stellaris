import pygame
import random
import math

class SolarSystem:
    """pretty self explanatory solar system object class"""
    def __init__(self, star_type, star_name):
        self.star_name = star_name
        self.star_type = star_type
        self.star_position = (0, 0) #star is at 0,0 in world space position
        self.planets = self._generate_planets()

    def _generate_planets(self):
        num_planets = random.randint(3, 8)  # Random number of planets
        planet_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        #add more planet properties/attributes here later
        planets = []

        for i in range(num_planets):
            orbital_radius = 100 + i * random.randint(80, 140)  # Distance from the star
            size = random.randint(5, 15)  # Random size of the planet
            color = random.choice(planet_colors)  # Random planet color
            speed = random.uniform(0.5, 1.5) / orbital_radius  # Speed decreases with radius
            angle = random.uniform(0, 2 * math.pi)  # Random initial position in orbit
            name = f"object {i + 1}"
            planets.append({
                "radius": orbital_radius,
                "size": size,
                "color": color,
                "speed": speed,
                "angle": angle,
                "name": name
            })

        return planets

    def update(self, time_delta):
        """Update planet positions based on orbital mechanics"""
        for planet in self.planets:
            planet["angle"] += planet["speed"] * time_delta #increment angle based on speed
            planet["angle"] %= 2 * math.pi  # Keep angle within 0 to 2π to avoid overflow

    def render_solarsystem(self, screen, camera):
        """draw the star and planets"""
        # Draw the star (converted to screen coordinates using camera)
        screen_star_x, screen_star_y = camera.apply(self.star_position[0], self.star_position[1])
        pygame.draw.circle(screen, (255, 255, 0), (int(screen_star_x), int(screen_star_y)), 40)

        # Draw planets
        for planet in self.planets:
            world_x = self.star_position[0] + math.cos(planet["angle"]) * planet["radius"]
            world_y = self.star_position[1] + math.sin(planet["angle"]) * planet["radius"]
            screen_x, screen_y = camera.apply(world_x, world_y)
            pygame.draw.circle(screen, planet["color"], (int(screen_x), int(screen_y)), int(planet["size"] * camera.zoom))

