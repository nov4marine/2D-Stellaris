class Camera:
    ZOOM_MIN = 0.075
    ZOOM_MAX = 5.0
    ZOOM_STEP = 0.2

    def __init__(self, screen_width, screen_height):
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
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

    def zoom_to(self, new_zoom, pivot):
        """
        Instantly zooms to the nearest allowed zoom level, keeping the world coordinate under the pivot fixed.
        :param new_zoom: Desired zoom level (float)
        :param pivot: (x, y) tuple for the pivot in screen coordinates.
        """
        # Snap to nearest allowed zoom step
        snapped_zoom = max(self.ZOOM_MIN, min(self.ZOOM_MAX, round(new_zoom / self.ZOOM_STEP) * self.ZOOM_STEP))
        pivot_x, pivot_y = pivot

        # World coordinates under the pivot before zoom
        world_x = self.offset_x + pivot_x / self.zoom
        world_y = self.offset_y + pivot_y / self.zoom

        # Update zoom
        self.zoom = snapped_zoom

        # Adjust offset so the same world coordinate stays under the cursor
        self.offset_x = world_x - pivot_x / self.zoom
        self.offset_y = world_y - pivot_y / self.zoom

    def set_zoom(self, zoom_factor):
        """Set zoom directly, snapping to nearest allowed step (no pivot adjustment)."""
        snapped_zoom = max(self.ZOOM_MIN, min(self.ZOOM_MAX, round(zoom_factor / self.ZOOM_STEP) * self.ZOOM_STEP))
        self.zoom = snapped_zoom

    def center_camera_on_star(self):
        """Center the camera on the star system you just clicked into."""
        self.offset_x = -(self.screen_width // 2)
        self.offset_y = -(self.screen_height // 2)
        self.zoom = 1.0

    def reset(self, offset_x, offset_y, zoom):
        """Reset camera settings (used for switching views)."""
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.set_zoom(zoom)

