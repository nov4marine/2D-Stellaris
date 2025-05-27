# src/galaxy.py
import scipy.spatial
import networkx as nx
import pygame
import random
import math
import os
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
        #self.owner = self.solar_system.owner
        self.rect = None  # For mouse collision/highlight
        self.selected = False  # For UI selection, etc.

    def get_position(self):
        return (self.x, self.y)

class Galaxy:
    TILE_SIZE = 512
    TILE_FOLDER = "2D-Stellaris/assets/galaxy_tiles"

    def __init__(self, galaxy_size=6000, num_stars=1000):
        self.galaxy_size = galaxy_size
        self.num_stars = num_stars
        self.galaxy_background = None
        self.low_res_galaxy = "2D-Stellaris/assets/M51_1k.png"

        # Step 1: Generate star positions and attributes (galaxy map only)
        self.galaxy_stars = self._generate_galaxy_stars(num_stars, galaxy_size)

        # Pre-render star bloom effects
        self.star_bloom = self._prerender_star_bloom()
        self._prerender_background()

        # Step 2: Generate solar systems and link to stars
        self.solar_systems = self._generate_solar_systems()

        # Step 4: Generate hyperlanes
        self.hyperlanes = self.generate_prim_hyperlanes()

        self.tile_cache = {}  # {(tx, ty): pygame.Surface}
        self.max_tile_cache = 32  # Limit RAM usage
        self._lowres_cache = {}

    def _generate_galaxy_stars(self, num_stars, galaxy_size):
        star_colors = [
            (255, 255, 0), (255, 0, 0), (0, 255, 0),
            (0, 0, 255), (255, 255, 255)
        ]
        stars = []

        num_arms = 4
        arm_tightness = 3  # Lower = looser, higher = tighter spiral
        arm_spread = 0.25    # Lower = thinner arms, higher = fuzzier arms
        center_radius = galaxy_size * 0.15
        overall_rotation = math.pi / 4
        min_distance = 200

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
            star.solar_system = solar_system  # Link back to the star
        return solar_systems
    

    def _prerender_star_bloom(self):
        """Pre-render blurred glow surfaces for each star"""
        bloom = pygame.Surface((300, 300), pygame.SRCALPHA)  # Create a surface with a transparent background
        for i in range(1, 12):
            surface = pygame.Surface((300, 300), pygame.SRCALPHA) # Create a surface with a transparent background
            pygame.draw.circle(surface, (255, 255, 255, 100), (300 // 2, 300 // 2), (i * 10)) #draw bloom circle
            surface.set_alpha(255 / i)
            self.star_bloom = surface
            bloom.blit(surface, (0, 0))  # Additive blending for bloom effect
        return bloom

    def _prerender_background(self):
        """Pre-render the galaxy background image"""
        self.galaxy_background = pygame.image.load(
            "C:/Users/nov4m/Documents/Python/Stellaris Github/2D-Stellaris/assets/galaxy_background.png"
        ).convert()
        self.galaxy_background = pygame.transform.scale(
            self.galaxy_background,
            (game_state["screen_width"], game_state["screen_height"])
        )

    def update_solar_systems(self, time_delta):
        for system in self.solar_systems.values():
            system.update(time_delta)

    # --- Tiled disk rendering in render_galaxy ---
    def render_galaxy(self, screen, camera):
        """Render the galaxy map with stars, hyperlanes, and background."""
        screen.blit(self.galaxy_background, (0, 0))

        # --- Galactic Disk (Tiled) ---
        # These should match your image and tiling
        image_pixel_size = 4207  # Actual size of your galaxy image (assume square)
        galaxy_world_size = self.galaxy_size * 2  # -galaxy_size to +galaxy_size

        tile_world_size = self.TILE_SIZE * (galaxy_world_size / image_pixel_size)

        # Calculate visible region in world coords
        left = camera.offset_x
        top = camera.offset_y
        right = left + camera.screen_width / camera.zoom
        bottom = top + camera.screen_height / camera.zoom

        # Figure out which tiles are visible
        tx_start = int(((left + self.galaxy_size) / galaxy_world_size) * image_pixel_size // self.TILE_SIZE)
        tx_end = int(((right + self.galaxy_size) / galaxy_world_size) * image_pixel_size // self.TILE_SIZE) + 1
        ty_start = int(((top + self.galaxy_size) / galaxy_world_size) * image_pixel_size // self.TILE_SIZE)
        ty_end = int(((bottom + self.galaxy_size) / galaxy_world_size) * image_pixel_size // self.TILE_SIZE) + 1

        if camera.zoom > 0.5:
            for ty in range(ty_start, ty_end):
                for tx in range(tx_start, tx_end):
                    tile_img = self.get_tile(tx, ty)
                    if tile_img is None:
                        continue
                    # Scale tile to cover correct world area at current zoom
                    scaled_tile_size = int(tile_world_size * camera.zoom)
                    # Compute world position of this tile's top-left
                    tile_pixel_x = tx * self.TILE_SIZE
                    tile_pixel_y = ty * self.TILE_SIZE
                    world_x = (tile_pixel_x / image_pixel_size) * galaxy_world_size - self.galaxy_size
                    world_y = (tile_pixel_y / image_pixel_size) * galaxy_world_size - self.galaxy_size
                    screen_x, screen_y = camera.apply(world_x, world_y)
                    screen.blit(pygame.transform.scale(tile_img, (scaled_tile_size, scaled_tile_size)), (screen_x, screen_y))

        else:
            # If zoomed out, draw the low-res galaxy image aligned with the galaxy area
            if camera.zoom not in self._lowres_cache:
                low_res_image = pygame.image.load(self.low_res_galaxy).convert()
                low_res_image.set_alpha(100)
                # Scale to cover the galaxy area in world coordinates
                scaled_size = int(self.galaxy_size * 2 * camera.zoom)
                low_res_image = pygame.transform.scale(low_res_image, (scaled_size, scaled_size))
                self._lowres_cache[camera.zoom] = low_res_image
            low_res_image = self._lowres_cache[camera.zoom]
            # Compute where (-galaxy_size, -galaxy_size) is on screen
            screen_x, screen_y = camera.apply(-self.galaxy_size, -self.galaxy_size)
            screen.blit(low_res_image, (screen_x, screen_y))

        # --- Bloom Layer & Stars ---
        screen_rect = pygame.Rect(0, 0, camera.screen_width, camera.screen_height)
        for star in self.galaxy_stars:
            screen_x, screen_y = camera.apply(star.x, star.y)
            star_radius = int(star.radius * camera.zoom)
            star_rect = pygame.Rect(
                int(screen_x - star_radius),
                int(screen_y - star_radius),
                int(star_radius * 2),
                int(star_radius * 2)
            )

            # Only draw stars/blooms if on screen
            if not screen_rect.colliderect(star_rect):
                continue

            # Draw bloom (always scale on demand, or keep your bloom cache logic if you want)
            bloom = self.star_bloom
            width = int(bloom.get_width() * camera.zoom)
            height = int(bloom.get_height() * camera.zoom)
            scaled_glow = pygame.transform.scale(bloom, (width, height))
            rect = scaled_glow.get_rect(center=(int(screen_x), int(screen_y)))
            screen.blit(scaled_glow, rect)

            # Draw star
            twinkle = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() / 500 + hash(star.name) % 100)
            radius = int(star.radius * camera.zoom * twinkle)
            pygame.draw.circle(screen, star.color, (int(screen_x), int(screen_y)), radius)

        # --- Stars Rects for Mouse Collision ---
        for star in self.galaxy_stars:
            screen_x, screen_y = camera.apply(star.x, star.y)
            star.rect = pygame.Rect(
                int(screen_x - star.radius * camera.zoom),
                int(screen_y - star.radius * camera.zoom),
                int(star.radius * 2 * camera.zoom),
                int(star.radius * 2 * camera.zoom)
            )

            # draw sovereignty map 
            #self.draw_sovereignty_voronoi(screen, camera)

        # --- HYPERLANES ---
        for line in self.hyperlanes:
            start, end = line
            start_x, start_y = camera.apply(start.x, start.y)
            end_x, end_y = camera.apply(end.x, end.y)
            pygame.draw.line(screen, (120, 180, 225), (start_x, start_y), (end_x, end_y), 1)

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

    def get_solar_system(self, star_name):
        return self.solar_systems.get(star_name)

    def update(self, time_delta):
        # Add logic for background events, sovereignty, etc.
        self.update_solar_systems(time_delta)

    def get_tile(self, tx, ty):
        key = (tx, ty)
        if key in self.tile_cache:
            return self.tile_cache[key]
        tile_path = os.path.join(self.TILE_FOLDER, f"tile_{tx}_{ty}.png")
        if not os.path.exists(tile_path):
            return None
        tile_img = pygame.image.load(tile_path).convert()
        tile_img.set_alpha(100)
        self.tile_cache[key] = tile_img
        # Simple LRU: evict oldest if cache too big
        if len(self.tile_cache) > self.max_tile_cache:
            self.tile_cache.pop(next(iter(self.tile_cache)))
        return tile_img

    def draw_sovereignty_voronoi(self, screen, camera):
        """Draw semi-transparent sovereignty regions using Voronoi polygons."""
        points = [(star.x, star.y) for star in self.galaxy_stars]
        if len(points) < 3:
            return  # Voronoi needs at least 3 points

        vor = scipy.spatial.Voronoi(points)
        # Map points to stars for color lookup
        pos_to_star = {(star.x, star.y): star for star in self.galaxy_stars}

        for point_idx, region_idx in enumerate(vor.point_region):
            region = vor.regions[region_idx]
            if -1 in region or len(region) == 0:
                continue  # Skip infinite regions

            polygon = [vor.vertices[i] for i in region]
            star = self.galaxy_stars[point_idx]
            # Choose color: use star.owner.color if available, else default
            if hasattr(star, "owner") and star.owner is not None:
                color = star.owner.color
            else:
                color = (120, 120, 120)  # Neutral/unclaimed

            # Make it semi-transparent
            overlay_color = (*color, 60)

            # Transform polygon points to screen coordinates
            screen_poly = [camera.apply(x, y) for x, y in polygon]

            # Draw the polygon on a temporary surface for alpha blending
            min_x = min(p[0] for p in screen_poly)
            min_y = min(p[1] for p in screen_poly)
            max_x = max(p[0] for p in screen_poly)
            max_y = max(p[1] for p in screen_poly)
            surf_w = int(max_x - min_x)
            surf_h = int(max_y - min_y)
            if surf_w < 1 or surf_h < 1:
                continue

            temp_surface = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
            shifted_poly = [(x - min_x, y - min_y) for x, y in screen_poly]
            pygame.draw.polygon(temp_surface, overlay_color, shifted_poly)
            screen.blit(temp_surface, (min_x, min_y))
