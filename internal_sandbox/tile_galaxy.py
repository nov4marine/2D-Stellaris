from PIL import Image
import os

TILE_SIZE = 512
img = Image.open("2D-Stellaris/assets/M51_1k.png")  # Use your high-res disk image
w, h = img.size

os.makedirs("tiles", exist_ok=True)

for y in range(0, h, TILE_SIZE):
    for x in range(0, w, TILE_SIZE):
        tile = img.crop((x, y, min(x + TILE_SIZE, w), min(y + TILE_SIZE, h)))
        tile.save(f"1k_tiles/tile_{x//TILE_SIZE}_{y//TILE_SIZE}.png")