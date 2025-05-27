# Save this as downscale_image.py and run it in the same folder as your image
from PIL import Image

# Path to your original image
input_path = "2D-Stellaris/assets/M51_1k.png"

# Path to save the downscaled image
output_path = "2D-Stellaris/assets/M51_0.5k.png"

# Open the image
img = Image.open(input_path)

# Choose a new size (e.g., 50% of original)
scale_factor = 0.5  # Change as needed
new_size = (int(img.width * scale_factor), int(img.height * scale_factor))

# Resize and save
img = img.resize(new_size, Image.LANCZOS)
img.save(output_path, optimize=True)

print(f"Saved downscaled image as {output_path} with size {new_size}")