class Camera:
    def __init__(self, screen_width, screen_height):
        self.offset_x = 0  # Camera's top-left corner x in world coordinates
        self.offset_y = 0  # Camera's top-left corner y in world coordinates
        self.zoom = 1.0  # Default zoom level
        self.target_zoom = 1 #target zoom level for smooth zooming
        self.target_offset_x = self.offset_x # Target offset x for smooth panning
        self.target_offset_y = self.offset_y # Target offset y for smooth panning
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        screen_x = (world_x - self.offset_x) * self.zoom
        screen_y = (world_y - self.offset_y) * self.zoom
        return screen_x, screen_y

    def move(self, dx, dy):
        """Move the camera by dx and dy in world coordinates."""
        self.target_offset_x += dx
        self.target_offset_y += dy

    def zoom_to(self, new_zoom, pivot):
        """
        Zooms towards the given pivot point (screen coordinates), ensuring that
        the world coordinate under the pivot remains the same.
        
        :param new_zoom: New target zoom level.
        :param pivot: (x, y) tuple for the pivot in screen coordinates.
        """
        pivot_x, pivot_y = pivot

        # Determine the world coordinates currently under the pivot:
        world_x = self.offset_x + pivot_x / self.zoom
        world_y = self.offset_y + pivot_y / self.zoom
        
        # Set the new target zoom:
        self.target_zoom = max(0.1, min(new_zoom, 5.0))  # Clamp to [0.1, 5.0]
        
        # Calculate the new target offsets so that the same world coordinate stays at pivot:
        self.target_offset_x = world_x - pivot_x / self.target_zoom
        self.target_offset_y = world_y - pivot_y / self.target_zoom

    def update_zoom(self):
        # Smooth interpolation speed (adjust factor as needed)
        smooth_factor = 0.2
        # Smoothly update zoom:
        self.zoom += (self.target_zoom - self.zoom) * smooth_factor
        # Smoothly update camera offsets:
        self.offset_x += (self.target_offset_x - self.offset_x) * smooth_factor
        self.offset_y += (self.target_offset_y - self.offset_y) * smooth_factor

    def set_zoom(self, zoom_factor):
        self.target_zoom = max(0.1, min(zoom_factor, 5.0))  # Clamp target_zoom within bounds

    def center_camera_on_star(self):
        """center the camera on the star system you just clicked into"""
        self.offset_x = -(self.screen_width // 2)  # Offset to center the star horizontally
        self.offset_y = -(self.screen_height // 2)  # Offset to center the star vertically
        self.zoom = 1.0  # Reset zoom to default

    def reset(self, offset_x, offset_y, zoom):
        """Reset camera settings (used for switching views)."""
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.target_zoom = zoom
        
