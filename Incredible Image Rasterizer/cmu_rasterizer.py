from PIL import Image as img
from sklearn.cluster import KMeans
import numpy as np

image_file_path = "C:/Users/344951520/Downloads/firefox2.jpg"  # Update this to your image file path

# Open the image file and convert it to a numpy array
image = img.open(image_file_path)
image_array = np.array(image)
generate_rainbow = False
width, height = image.size

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

    for y in range(height):
        x = 0
        while x < width:
            current_color = image_array[y, x][:3]
            start_x = x
            
            # Move x to the end of the line of the same color
            while x < width and np.array_equal(image_array[y, x][:3], current_color):
                x += 1

            line_length = x - start_x

            # For both dots and lines, we use Rect. Dots are simply 1x1 Rects.
            color_str = f"rgb({current_color[0]}, {current_color[1]}, {current_color[2]})"
            if line_length == 1:
                instructions.append(f"Rect({start_x}, {y}, 1, 1, fill={color_str})")
            else:
                instructions.append(f"Rect({start_x}, {y}, {line_length}, 1, fill={color_str})")

    return instructions

instructions = generate_drawing_instructions(new_image_array)

# Save the lines of code to a file
file_name = "Incredible Image Rasterizer/rasterized_image_output.py"
with open(file_name, "w") as file:
    file.write(f"# The code for this drawing was generated by Jacob Barr\'s incredible CMU Graphics Image Rasterizer!\n# https://github.com/jbsparrow/CMU-Python-Academy/blob/main/Incredible%20Image%20Rasterizer/cmu_rasterizer.py\n")
    if generate_rainbow:
        file.write("from colorsys import hsv_to_rgb\n\napp.stepsPerSecond=60\napp.hue=0\napp.hueStep=0.01\n")
    file.write(f"app.setMaxShapeCount(4096)\napp.background = rgb(0,0,0)\n\nwidth={width}\nheight={height}\n\n\n")
    for instruction in instructions:
        file.write(f"{instruction}\n")

    file.write("\n\n# Move drawing to the center of the canvas\nfor i in app.group:\n\ti.left+=200-width/2\n\ti.top+=200-height/2")
    if generate_rainbow:
        file.write("\n\n\ndef onStep():\n\tfor i in app.group:\n\t\ti.fill=rgb(*hsv_to_rgb(app.hue,1,255))\n\tapp.hue+=app.hueStep\n\tif app.hue>1:\n\t\tapp.hue=0")

print(f"Rasterized image saved to {file_name}")
