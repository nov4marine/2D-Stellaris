import pygame
import random
import math
from src.game_state import game_state

class SolarSystem:
    """Container for all celestial bodies in a system (star, planets, moons, asteroids, etc.)"""
    def __init__(self, name, owner=None, bodies=None):
        self.name = name
        self.owner = owner
        self.bodies = bodies if bodies is not None else self._generate_bodies()

    def change_owner(self, new_owner):
        """Change the owner of the solar system."""
        self.owner = new_owner 

    def _generate_bodies(self):
        bodies = []

        # --- Generate the star ---
        star_type = random.choice(["G", "K", "M", "F", "A"])
        star = Star(
            name=f"{self.name} Star",
            star_type=star_type,
            radius=0,  # At system center
            size=40,
            color=None,  # Will be set by Star class based on type
            angle=0,
            speed=0,
            parent=None
        )
        bodies.append(star)

        # --- Generate planets ---
        num_planets = random.randint(4, 10)
        for i in range(num_planets):
            orbital_radius = 600 * (1.5 ** i)
            distance_ratio = orbital_radius / 10000
            planet_type = self.determine_planet_type(distance_ratio)
            size = random.randint(5, 10) if planet_type == "rocky" else random.randint(10, 20)
            color = None  # Let Planet class pick based on type, or randomize here
            speed = random.uniform(0.5, 1.5) / orbital_radius * 0.5
            angle = random.uniform(0, 2 * math.pi)
            name = f"{self.name} Planet {i+1}"
            planet = Planet(
                name=name,
                radius=orbital_radius,
                size=size,
                color=color,
                angle=angle,
                speed=speed,
                parent=star,
                type=planet_type
            )
            bodies.append(planet)

            # --- Optionally generate moons for some planets ---
            if planet_type == "rocky" and random.random() < 0.4:
                num_moons = random.randint(1, 2)
                for m in range(num_moons):
                    moon_radius = planet.size * 3 + random.randint(10, 30)
                    moon_angle = random.uniform(0, 2 * math.pi)
                    moon = Moon(
                        name=f"{planet.name} Moon {m+1}",
                        radius=moon_radius,
                        size=random.randint(2, 5),
                        color=(180, 180, 180),
                        angle=moon_angle,
                        speed=random.uniform(0.001, 0.003),
                        parent=planet
                    )
                    bodies.append(moon)

             # --- Optionally generate moons for gas giants ---
            if planet_type == "gas" and random.random() < 0.8:
                num_moons = random.randint(1, 8)
                for m in range(num_moons):
                    moon_radius = planet.size * 3 + random.randint(10, 30)
                    moon_angle = random.uniform(0, 2 * math.pi)
                    moon = Moon(
                        name=f"{planet.name} Moon {m+1}",
                        radius=moon_radius,
                        size=random.randint(2, 5),
                        color=(180, 180, 180),
                        angle=moon_angle,
                        speed=random.uniform(0.001, 0.003),
                        parent=planet
                    )
                    bodies.append(moon)

        # --- Optionally generate asteroids ---
        for _ in range(random.randint(10, 20)):
            belt_radius = random.uniform(1500, 3000)
            belt_angle = random.uniform(0, 2 * math.pi)
            asteroid = Asteroid(
                name=f"{self.name} Asteroid",
                radius=belt_radius,
                size=random.randint(1, 3),
                color=(120, 120, 120),
                angle=belt_angle,
                speed=random.uniform(0.0005, 0.0015),
                parent=star
            )
            #bodies.append(asteroid)

        return bodies

    def determine_planet_type(self, distance_ratio):
        weights = [
            max(0, 1.0 - distance_ratio * 2),  # Rocky more likely closer in
            max(0, distance_ratio),            # Gas more likely farther out
            max(0, distance_ratio - 0.5)       # Icy dominant in outer regions
        ]
        return random.choices(["rocky", "gas", "icy"], weights=weights, k=1)[0]

    def update(self, time_delta):
        for body in self.bodies:
            body.update_orbit(time_delta)

    def render(self, screen, camera):
        # Draw background
        screen.fill((10, 10, 30))  # Example: dark space background

        # Draw faint orbital rings for orbiting bodies
        for body in self.bodies:
            if body.parent is not None:
                parent_pos = body.parent.get_position()
                world_x, world_y = parent_pos
                screen_x, screen_y = camera.apply(world_x, world_y)
                # Draw a faint ring for the orbit
                pygame.draw.circle(
                    screen,
                    (100, 100, 140),  # Faint blue-gray color
                    (int(screen_x), int(screen_y)),
                    int(body.radius * camera.zoom),
                    1  # Thin line
                )

        # Draw all bodies (stars, planets, moons, asteroids)
        for body in self.bodies:
            if body.parent is not None:
                parent_pos = body.parent.get_position()
            else:
                parent_pos = (0, 0)  # System center
            body.draw(screen, camera, parent_pos)

    def get_star(self):
        return next((b for b in self.bodies if b.body_type == "star"), None)

    def get_planets(self):
        return [b for b in self.bodies if b.body_type == "planet"]

    def get_moons(self):
        return [b for b in self.bodies if b.body_type == "moon"]

    def get_asteroids(self):
        return [b for b in self.bodies if b.body_type == "asteroid"]

    @staticmethod
    def assign_capital_system(galaxy, nation):
        """
        Assigns a random SolarSystem and planet as the nation's homeworld.
        Modifies the planet to be habitable and sets its properties.
        Returns (planet, system_name).
        """
        # Pick a random SolarSystem that is not already owned
        unowned_systems = [s for s in galaxy.solar_systems.values() if s.owner is None]
        if not unowned_systems:
            raise Exception("No unowned solar systems available for capital assignment.")
        system = random.choice(unowned_systems)
        system.owner = nation

        # Prefer rocky planets, fallback to any planet
        rocky_planets = [p for p in system.get_planets() if getattr(p, "type", None) == "rocky"]
        if rocky_planets:
            planet = random.choice(rocky_planets)
        else:
            planets = system.get_planets()
            if not planets:
                raise Exception(f"No planets found in system {system.name}")
            planet = random.choice(planets)

        # Set planet as habitable and assign properties
        planet.habitable = True
        planet.name = nation.homeworld["homeworld"]["planet"]
        planet.climate = nation.homeworld["homeworld"]["climate"]
        planet.color = (0, 255, 255)  # Optional: visually mark as habitable

        return planet, system.name

# --- Celestial Body Classes ---

class CelestialBody:
    def __init__(self, name, body_type, radius, size, color, angle, speed, parent=None, **kwargs):
        self.name = name
        self.body_type = body_type
        self.radius = radius
        self.size = size
        self.color = color or (255, 255, 255)
        self.angle = angle
        self.speed = speed
        self.parent = parent  # Another CelestialBody or None
        self.rect = None  # For mouse collision/highlight
        for k, v in kwargs.items():
            setattr(self, k, v)

    def update_orbit(self, time_delta):
        self.angle += self.speed * time_delta
        self.angle %= 2 * math.pi

    def get_position(self):
        """Return world position relative to system center."""
        if self.parent is None:
            return (0, 0)
        parent_x, parent_y = self.parent.get_position()
        x = parent_x + math.cos(self.angle) * self.radius
        y = parent_y + math.sin(self.angle) * self.radius
        return (x, y)

    def draw(self, screen, camera, parent_pos):
        world_x, world_y = self.get_position()
        screen_x, screen_y = camera.apply(world_x, world_y)
        radius = int(self.size * camera.zoom)
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), radius)
        # Update rect for mouse collision
        self.rect = pygame.Rect(
            int(screen_x - radius),
            int(screen_y - radius),
            radius * 2,
            radius * 2
        )

class Star(CelestialBody):
    STAR_COLORS = {
        "O": (155, 176, 255),
        "B": (170, 191, 255),
        "A": (202, 215, 255),
        "F": (248, 247, 255),
        "G": (255, 244, 234),
        "K": (255, 210, 161),
        "M": (255, 204, 111),
    }
    def __init__(self, name, star_type, radius, size, color=None, angle=0, speed=0, parent=None, **kwargs):
        color = color or self.STAR_COLORS.get(star_type, (255, 255, 255))
        super().__init__(name, "star", radius, size, color, angle, speed, parent, star_type=star_type, **kwargs)
        self.star_type = star_type

    def get_position(self):
        return (0, 0)  # Always at system center

    def draw(self, screen, camera, parent_pos):
        # Custom star drawing (glow, etc.) can go here
        world_x, world_y = self.get_position()
        screen_x, screen_y = camera.apply(world_x, world_y)
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), int(self.size * camera.zoom))

class Planet(CelestialBody):
    def __init__(self, name, radius, size, color, angle, speed, parent, resources=None, type="rocky", habitable=False, climate=None, colony=None, **kwargs):
        color = color or ((100, 200, 255) if type == "rocky" else (200, 200, 100))
        super().__init__(name, "planet", radius, size, color, angle, speed, parent, type=type, **kwargs)
        self.type = type
        self.habitable = habitable
        self.climate = climate
        self.colony = colony
        self.resources = resources # Probably a dictionary of resources and their amounts. will create a function for procedural generation of resources later

class Moon(CelestialBody):
    def __init__(self, name, radius, size, color, angle, speed, parent, **kwargs):
        super().__init__(name, "moon", radius, size, color, angle, speed, parent, **kwargs)

class Asteroid(CelestialBody):
    def __init__(self, name, radius, size, color, angle, speed, parent, **kwargs):
        super().__init__(name, "asteroid", radius, size, color, angle, speed, parent, **kwargs)


