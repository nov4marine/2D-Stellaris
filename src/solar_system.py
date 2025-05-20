import pygame
import random
import math

class SolarSystem:
    """pretty self explanatory solar system object class"""
    def __init__(self, star_type, star_name, max_radius=10000, planets=None):
        self.star_name = star_name
        self.star_type = star_type
        self.star_position = (0, 0) #star is at 0,0 in world space position
        self.max_radius = max_radius  # Maximum distance from the star
        if planets is not None:
            self.planets = planets
        else:
            self.planets = self._generate_planets()

    def _generate_planets(self):
        num_planets = random.randint(4, 10)  # Random number of planets
        planet_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
        #add more planet properties/attributes here later
        planets = []

        for i in range(num_planets):
            orbital_radius = 200 * (1.5 ** i) * random.uniform(0.9, 1.1)  # Distance from the star
            distance_ratio = orbital_radius / self.max_radius  # Normalize distance relative to system size
            planet_type = self.determine_planet_type(distance_ratio)  # Determine planet type based on distance

            size = random.randint(5, 10) if type == "rocky" else random.randint(10,20) # Random size of the planet
            color = random.choice(planet_colors)  # Random planet color
            speed = random.uniform(0.5, 1.5) / orbital_radius * 0.5  # Orbital speed based on distance
            angle = random.uniform(0, 2 * math.pi)  # Random initial position in orbit
            name = f"object {i + 1}"
            planets.append({
                "radius": orbital_radius,
                "size": size,
                "type": planet_type,
                "color": color,
                "speed": speed,
                "angle": angle,
                "name": name,
                "habitable": False,
                "colony": None,  # Placeholder for colony object
            })

        # add a 20% chance to make one rocky planet habitable
        if random.random() < 0.2:
            habitable_planet = random.choice([p for p in planets if p["type"] == "rocky"])
            habitable_planet["habitable"] = True
            habitable_planet["color"] = (0, 255, 255)

        return planets
    
    def determine_planet_type(self, distance_ratio):
        """
        Weighted probabilities for planet types based on distance ratio.
        """
        weights = [
            max(0, 1.0 - distance_ratio * 2),  # Rocky more likely closer in
            max(0, distance_ratio),            # Gas more likely farther out
            max(0, distance_ratio - 0.5)       # Icy dominant in outer regions
        ]
        return random.choices(["rocky", "gas", "icy"], weights=weights, k=1)[0]

    def update(self, time_delta):
        """Update planet positions based on orbital mechanics"""
        for planet in self.planets:
            planet["angle"] += planet["speed"] * time_delta #increment angle based on speed
            planet["angle"] %= 2 * math.pi  # Keep angle within 0 to 2π to avoid overflow

    def render_solarsystem(self, screen, camera, selected_star):
        """draw the star and planets"""
        # Draw the star (converted to screen coordinates using camera)
        screen_star_x, screen_star_y = camera.apply(self.star_position[0], self.star_position[1])
        pygame.draw.circle(screen, (255, 255, 0), (int(screen_star_x), int(screen_star_y)), 40 * camera.zoom)  # Draw the star

        # Draw faint orbital rings
        for planet in self.planets:
            # Calculate screen position for the orbital radius
            screen_x, screen_y = camera.apply(self.star_position[0], self.star_position[1])
            orbital_radius = planet["radius"] * camera.zoom
            
            # Draw a thin circle outline for the orbital ring
            ring_color = (200, 200, 200)  # Light gray
            pygame.draw.circle(screen, ring_color, (int(screen_x), int(screen_y)), int(orbital_radius), 1)

        # Draw planets
        for planet in self.planets:
            world_x = self.star_position[0] + math.cos(planet["angle"]) * planet["radius"]
            world_y = self.star_position[1] + math.sin(planet["angle"]) * planet["radius"]
            screen_x, screen_y = camera.apply(world_x, world_y)
            pygame.draw.circle(screen, planet["color"], (int(screen_x), int(screen_y)), int(planet["size"] * camera.zoom))

    def create_capital_system(star_name="Sol", star_type="G-type", max_radius=10000):
        #This function will later be expanded or copied to be capable of generating a customized solar system 
        # Example: 5 planets, 3rd is habitable
        planets = []
        for i in range(5):
            planet_type = "rocky" if i < 3 else "gas"
            planet = {
                "radius": 200 * (i + 1),
                "size": 10 if planet_type == "rocky" else 20,
                "type": planet_type,
                "color": (0, 255, 255) if i == 2 else (150, 150, 150),
                "speed": 0.001 * (i + 1),
                "angle": 0,
                "name": f"Capital Planet {i+1}",
                "habitable": (i == 2),  # Only the 3rd planet is habitable
            }
            planets.append(planet)
        return SolarSystem(star_type=star_type, star_name=star_name, max_radius=max_radius, planets=planets)

    def assign_capital_system(galaxy, nation_params):
        # 1. Pick a random star (or use a selection method)
        candidate_stars = [star for star in galaxy.stars if star["name"] not in ["Sol", "Alpha Centauri"]]  # Optionally filter
        chosen_star = random.choice(candidate_stars)
        star_name = chosen_star["name"]

        # 2. Get the corresponding solar system
        system = galaxy.solar_systems[star_name]

        # 3. Find a rocky planet to be the capital
        rocky_planets = [p for p in system.planets if p["type"] == "rocky"]
        if rocky_planets:
            capital_planet = random.choice(rocky_planets) # Pick a random rocky planet
            capital_planet["habitable"] = True # Mark it as habitable
            capital_planet["name"] = nation_params["homeworld"]["planet"] # Use the name from nation_params
            capital_planet["climate"] = nation_params["homeworld"]["climate"] # Use the climate from nation_params
            capital_planet["color"] = (0, 255, 255)  # Visually distinct
        else:
            # Fallback: just use the 3rd planet
            system.planets[3]["habitable"] = True
            system.planets[3]["name"] = nation_params["homeworld"]["planet"]
            system.planets[3]["climate"] = nation_params["homeworld"]["climate"]
            system.planets[3]["color"] = (0, 255, 255)

        # 4. Optionally, store the capital system/star name in the nation/player data
        return capital_planet, star_name  # So you can reference it as the capital

