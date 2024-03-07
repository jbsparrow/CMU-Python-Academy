from PIL import Image as img
from sklearn.cluster import KMeans
import numpy as np

image_file_path = "C:/Users/344951520/Downloads/firefox2.jpg"  # Update this to your image file path

# Open the image file and convert it to a numpy array
image = img.open(image_file_path)
image_array = np.array(image)
width, height = image.size

generate_rainbow = True

# Ensure we work with RGBA for uniformity
if image_array.shape[2] == 3:
    image_array = np.dstack([image_array, np.ones((image_array.shape[0], image_array.shape[1], 1)) * 255]).astype(np.uint8)

# Flatten the image array and apply k-means clustering to reduce to 8 colors
pixels = image_array.reshape((-1, 4))
kmeans = KMeans(n_clusters=8, random_state=0).fit(pixels)
new_pixels = kmeans.cluster_centers_[kmeans.labels_].round().astype(int)

# Reshape back to the original image shape
new_image_array = new_pixels.reshape(image_array.shape)

# Function to generate simplified drawing instructions using Rect() for dots and lines
def generate_drawing_instructions(image_array):
    height, width, _ = image_array.shape
    instructions = []
    merged_blocks = []

    # First, generate horizontal lines
    for y in range(height):
        x = 0
        while x < width:
            current_color = image_array[y, x][:3]
            start_x = x
            
            while x < width and np.array_equal(image_array[y, x][:3], current_color):
                x += 1

            line_length = x - start_x
            color_str = f"rgb({current_color[0]}, {current_color[1]}, {current_color[2]})"
            block = {"x": start_x, "y": y, "width": line_length, "height": 1, "color": color_str}
            merged_blocks.append(block)

    # Then, attempt to merge vertically
    final_blocks = []
    while merged_blocks:
        base = merged_blocks.pop(0)
        i = 0
        while i < len(merged_blocks):
            other = merged_blocks[i]
            if base["x"] == other["x"] and base["width"] == other["width"] and base["color"] == other["color"] and base["y"] + base["height"] == other["y"]:
                base["height"] += other["height"]
                merged_blocks.pop(i)
            else:
                i += 1
        final_blocks.append(base)

    for block in final_blocks:
        instructions.append(f"Rect({block['x']}, {block['y']}, {block['width']}, {block['height']}, fill={block['color']})")

    return instructions

instructions = generate_drawing_instructions(new_image_array)

# Save the drawing instructions to a file
file_name = "Incredible Image Rasterizer/rasterized_image_output.py"
with open(file_name, "w") as file:
    # File header and setup
    file.write(f"# The code for this drawing was generated by Jacob Barr\'s incredible CMU Graphics Image Rasterizer!\n# https://github.com/jbsparrow/CMU-Python-Academy/blob/main/Incredible%20Image%20Rasterizer/cmu_rasterizer.py\n")
    if generate_rainbow:
        file.write("from colorsys import hsv_to_rgb, rgb_to_hsv\n\napp.stepsPerSecond=60\napp.hue=0\napp.hueStep=0.01\n")
    file.write(f"app.setMaxShapeCount(4096)\napp.background = rgb(0,0,0)\n\nwidth={width}\nheight={height}\n\n\n")

    # Writing instructions
    for instruction in instructions:
        file.write(f"{instruction}\n")

    # Footer for adjusting the drawing position
    file.write("\n\n# Move drawing to the center of the canvas\nfor i in app.group:\n\ti.left+=rounded(200-width/2)\n\ti.top+=rounded(200-height/2)")
    if generate_rainbow:
        file.write("\n\n\ndef onStep():\n\tfor i in app.group:\n\t\ti.fill=rgb(*hsv_to_rgb(app.hue,1,255))\n\tapp.hue+=app.hueStep\n\tif app.hue>1:\n\t\tapp.hue=0")

print(f"Drawing instructions saved to {file_name}")

