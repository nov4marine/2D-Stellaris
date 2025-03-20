class Camera:
    def __init__(self, screen_width, screen_height):
        self.offset_x = 0  # Camera's top-left corner x in world coordinates
        self.offset_y = 0  # Camera's top-left corner y in world coordinates
        self.zoom = 1.0  # Default zoom level
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        screen_x = (world_x - self.offset_x) * self.zoom
        screen_y = (world_y - self.offset_y) * self.zoom
        return screen_x, screen_y

    def move(self, dx, dy):
        """Move the camera by dx and dy in world coordinates."""
        self.offset_x += dx
        self.offset_y += dy

    def set_zoom(self, zoom_factor):
        """Set the zoom level, ensuring it stays within a valid range."""
        self.zoom = max(0.1, min(zoom_factor, 5.0))  # Clamp zoom between 0.1 and 5.0


    def center_camera_on_star(self, camera, screen_width, screen_height):
        """center the camera on the star system you just clicked into"""
        camera.offset_x = -(screen_width // 2)  # Offset to center the star horizontally
        camera.offset_y = -(screen_height // 2)  # Offset to center the star vertically
        camera.zoom = 1.0  # Reset zoom to default

    def reset(self, offset_x, offset_y, zoom):
        """Reset camera settings (used for switching views)."""
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.zoom = zoom
        
