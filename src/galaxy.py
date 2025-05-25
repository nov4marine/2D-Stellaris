# src/galaxy.py
import scipy.spatial
import networkx as nx
import pygame
import random
import math
from src.solar_system import SolarSystem
from src.game_state import game_state

class GalaxyStar:
    """
    Represents a star on the galaxy map.
    Holds galaxy coordinates, color, radius, and a reference to its SolarSystem.
    """
    def __init__(self, name, x, y, radius, color, solar_system=None):
        self.name = name
        self.x = x  # Galaxy map X
        self.y = y  # Galaxy map Y
        self.radius = radius
        self.color = color
        self.solar_system = solar_system  # Reference to SolarSystem object
        self.rect = None  # For mouse collision/highlight
        self.selected = False  # For UI selection, etc.

    def get_position(self):
        return (self.x, self.y)

class Galaxy:
    def __init__(self, galaxy_size=8000, num_stars=1000):
        self.galaxy_size = galaxy_size
        self.num_stars = num_stars
        self.galaxy_background = None

        # Step 1: Generate star positions and attributes (galaxy map only)
        self.galaxy_stars = self._generate_galaxy_stars(num_stars, galaxy_size)

        # Pre-render the galactic disk surface
        self._render_disk()

        # Pre-render star bloom effects
        self._render_star_bloom()

        # Step 2: Generate solar systems and link to stars
        self.solar_systems = self._generate_solar_systems()

        # Step 3: Link GalaxyStar objects to their SolarSystem
        for star in self.galaxy_stars:
            star.solar_system = self.solar_systems[star.name]

        # Step 4: Generate hyperlanes
        self.hyperlanes = self.generate_prim_hyperlanes()

    def _generate_galaxy_stars(self, num_stars, galaxy_size):
        star_colors = [
            (255, 255, 0), (255, 0, 0), (0, 255, 0),
            (0, 0, 255), (255, 255, 255)
        ]
        stars = []

        num_arms = 4
        arm_tightness = 3  # Lower = looser, higher = tighter spiral
        arm_spread = 0.25    # Lower = thinner arms, higher = fuzzier arms
        center_radius = galaxy_size * 0.1
        overall_rotation = math.pi / 4
        min_distance = 100

        for i in range(num_stars):
            while True:
                # Radial distance (ensuring it's outside the empty center)
                r = random.uniform(center_radius, galaxy_size)

                # Angle for the spiral arms
                arm_index = i % num_arms
                arm_angle = arm_index * (2 * math.pi / num_arms)
                # Add a small random offset to theta for spread
                theta_offset = random.gauss(0, arm_spread)
                theta = overall_rotation + arm_angle + arm_tightness * math.log(r + 1) + theta_offset

                # Convert polar to Cartesian
                x = r * math.cos(theta)
                y = r * math.sin(theta)

                # Check minimum distance to other stars
                too_close = False
                for star in stars:
                    distance = math.sqrt((x - star.x) ** 2 + (y - star.y) ** 2)
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

            stars.append(GalaxyStar(
                name=name,
                x=x,
                y=y,
                radius=radius,
                color=color
            ))
        return stars

    def _generate_solar_systems(self):
        """
        Create a SolarSystem for each GalaxyStar.
        The SolarSystem does NOT need to know its galaxy coordinates.
        """
        solar_systems = {}
        for star in self.galaxy_stars:
            # Only pass name and any system-specific args.
            solar_system = SolarSystem(
                name=star.name
                # You can add owner or other args if needed
            )
            solar_systems[star.name] = solar_system
        return solar_systems
    
    def _render_disk(self):
        """pre render the galactic disk surface"""
        self.disk_image = pygame.image.load(
            "2D-Stellaris/assets/M51.png"
        ).convert_alpha()
        self.disk_image = pygame.transform.scale(
            self.disk_image, (self.galaxy_size * 2, self.galaxy_size * 2)
        )

    
    def _render_star_bloom(self):
        """pre render blurred glow surfaces for each star"""
        self.star_bloom = {}
        for radius in range(10, 40):
            size = radius * 8 # radius of the surface upon which the bloom is drawn, not radius of the bloom
            # Create a surface with a transparent background
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 255, 255, 100), (size // 2, size // 2), radius * 3)
            bloom = pygame.transform.gaussian_blur(surface, 10)
            self.star_bloom[radius] = bloom

    def update_solar_systems(self, time_delta):
        for system in self.solar_systems.values():
            system.update(time_delta)

    def render_galaxy(self, screen, camera):
        # Draw the background
        if self.galaxy_background is None:
            self.galaxy_background = pygame.image.load(
                "C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/galaxy_background.png"
            ).convert()
            self.galaxy_background = pygame.transform.scale(
                self.galaxy_background,
                (game_state["screen_width"], game_state["screen_height"])
            )
        screen.blit(self.galaxy_background, (0, 0))

        # --- Galactic Disk ---
        # Center the disk at (0, 0) in world coordinates
        disk_center_screen = camera.apply(0, 0)
        disk_width = int(self.disk_image.get_width() * camera.zoom)
        disk_height = int(self.disk_image.get_height() * camera.zoom)
        scaled_disk = pygame.transform.scale(self.disk_image, (disk_width, disk_height))
        disk_rect = scaled_disk.get_rect(center=(int(disk_center_screen[0]), int(disk_center_screen[1])))
        screen.blit(scaled_disk, disk_rect)

        # --- Bloom Layer ---
        for star in self.galaxy_stars:
            screen_x, screen_y = camera.apply(star.x, star.y)
            # Pick the closest pre-rendered glow by star.radius
            base_radius = min(self.star_bloom.keys(), key=lambda r: abs(r - int(star.radius)))
            glow = self.star_bloom[base_radius]
            # Optionally scale for zoom
            scale = star.radius * camera.zoom / base_radius
            if scale != 1.0:
                glow = pygame.transform.smoothscale(glow, (int(glow.get_width() * scale), int(glow.get_height() * scale)))
            # Center the glow
            rect = glow.get_rect(center=(int(screen_x), int(screen_y)))
            screen.blit(glow, rect)

        # --- HYPERLANES ---
        for line in self.hyperlanes:
            start, end = line
            start_x, start_y = camera.apply(start.x, start.y)
            end_x, end_y = camera.apply(end.x, end.y)
            pygame.draw.line(screen, (120, 180, 225), (start_x, start_y), (end_x, end_y), 1)

        # --- STARS ---
        for star in self.galaxy_stars:
            screen_x, screen_y = camera.apply(star.x, star.y)
            # Twinkle
            twinkle = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() / 500 + hash(star.name) % 100)
            radius = int(star.radius * camera.zoom * twinkle)
            pygame.draw.circle(screen, star.color, (int(screen_x), int(screen_y)), radius)
            # Update rect for collision
            star.rect = pygame.Rect(
                int(screen_x - star.radius * camera.zoom),
                int(screen_y - star.radius * camera.zoom),
                int(star.radius * 2 * camera.zoom),
                int(star.radius * 2 * camera.zoom)
            )

    def generate_delaunay_hyperlanes(self, max_connections=3):
        points = [(star.x, star.y) for star in self.galaxy_stars]
        tri = scipy.spatial.Delaunay(points)
        G = nx.Graph()
        star_connections = {point: [] for point in points}

        for simplex in tri.simplices:
            for i in range(3):
                start = points[simplex[i]]
                end = points[simplex[(i + 1) % 3]]
                distance = math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
                G.add_edge(start, end, weight=distance)

        mst_edges = list(nx.minimum_spanning_edges(G, algorithm="kruskal", data=False))
        for start, end in mst_edges:
            star_connections[start].append(end)
            star_connections[end].append(start)

        for simplex in tri.simplices:
            for i in range(3):
                start = points[simplex[i]]
                end = points[simplex[(i + 1) % 3]]
                if len(star_connections[start]) < max_connections and len(star_connections[end]) < max_connections:
                    star_connections[start].append(end)
                    star_connections[end].append(start)

        # Convert to GalaxyStar objects
        pos_to_star = {(star.x, star.y): star for star in self.galaxy_stars}
        hyperlanes = []
        for start in star_connections:
            for end in star_connections[start]:
                hyperlanes.append((pos_to_star[start], pos_to_star[end]))
        return hyperlanes

    def generate_prim_hyperlanes(self):
        points = [(star.x, star.y) for star in self.galaxy_stars]
        G = nx.Graph()
        for i, start in enumerate(points):
            for j, end in enumerate(points):
                if i == j:
                    continue
                distance = math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
                G.add_edge(start, end, weight=distance)
        mst = nx.minimum_spanning_tree(G, algorithm="prim", weight="weight")
        pos_to_star = {(star.x, star.y): star for star in self.galaxy_stars}
        hyperlanes = []
        for start, end in mst.edges:
            hyperlanes.append((pos_to_star[start], pos_to_star[end]))
        return hyperlanes

    def generate_voronoi_hyperlanes(self):
        points = [(star.x, star.y) for star in self.galaxy_stars]
        vor = scipy.spatial.Voronoi(points)
        hyperlanes = []
        for ridge in vor.ridge_vertices:
            if -1 in ridge:
                continue
            start = vor.vertices[ridge[0]]
            end = vor.vertices[ridge[1]]
            hyperlanes.append((start, end))
        return hyperlanes

    def get_solar_system(self, star_name):
        return self.solar_systems.get(star_name)

    def update(self, time_delta):
        # Add logic for background events, sovereignty, etc.
        self.update_solar_systems(time_delta)
