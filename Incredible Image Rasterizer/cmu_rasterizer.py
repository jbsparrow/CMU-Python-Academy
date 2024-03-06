from PIL import Image as img
from PIL import ImageFilter
import numpy as np

image_file_path = "C:/Users/344951520/Downloads/cheese.png"

# Open the image file, resize it to fit the canvas, and convert it to a numpy array
canvas_size = (64,64)
image = img.open(image_file_path).filter(ImageFilter.SHARPEN).filter(ImageFilter.SHARPEN).resize(canvas_size, img.BICUBIC)
image_array = np.array(image)
width,height=image.size


generate_rainbow = False


# Check if image has opacity, if it does not, add an alpha channel that is always 255
if image_array.shape[2] == 3:
    image_array = np.dstack([image_array, np.full((image_array.shape[0], image_array.shape[1]), 255)])


def find_horizontal_merges(image_array):
    rectangles = []
    for i in range(image_array.shape[0]):
        j = 0
        while j < image_array.shape[1]:
            start_j = j
            while j < image_array.shape[1] and np.array_equal(image_array[i, j], image_array[i, start_j]):
                j += 1
            width = j - start_j
            r, g, b, a = image_array[i, start_j]
            if a > 0:  # Only consider non-transparent pixels
                opacity = int(a / 255 * 100)
                rectangles.append({"x": start_j, "y": i, "width": width, "height": 1, "color": (r, g, b, opacity)})
            j += 1
    return rectangles

def merge_vertical(rectangles):
    merged_rectangles = []
    while rectangles:
        base = rectangles.pop(0)
        i = 0
        while i < len(rectangles):
            rect = rectangles[i]
            if rect["x"] == base["x"] and rect["width"] == base["width"] and rect["color"] == base["color"] and rect["y"] == base["y"] + base["height"]:
                base["height"] += rect["height"]
                rectangles.pop(i)
            else:
                i += 1
        merged_rectangles.append(base)
    return merged_rectangles

def convert_to_code(rectangles):
    lines_of_code = []
    for rect in rectangles:
        r, g, b, opacity = rect["color"]
        lines_of_code.append(f"Rect({rect['x']}, {rect['y']}, {rect['width']}, {rect['height']}, fill=rgb({r}, {g}, {b}), opacity={opacity})")
    return lines_of_code

# Find horizontal merges first
horizontal_merged = find_horizontal_merges(image_array)
# Then attempt to merge these horizontally merged rectangles vertically
final_rectangles = merge_vertical(horizontal_merged)
# Convert the merged rectangles to lines of code
lines_of_code = convert_to_code(final_rectangles)

# Save the lines of code to a file
file_name = "Incredible Image Rasterizer/rasterized_image_output.py"
with open(file_name, "w") as file:
    file.write(f"# The code for this drawing was generated by Jacob Barr\'s incredible CMU Graphics Image Rasterizer!\n# https://github.com/jbsparrow/CMU-Python-Academy/blob/main/Incredible%20Image%20Rasterizer/cmu_rasterizer.py\n")
    if generate_rainbow:
        file.write("from colorsys import hsv_to_rgb\n\napp.stepsPerSecond=60\napp.hue=0\napp.hueStep=0.01\n")
    file.write(f"app.setMaxShapeCount(4096)\napp.background = rgb(0,0,0)\n\nwidth={width}\nheight={height}\n\n\n")
    for line in lines_of_code:
        file.write(f"{line}\n")

    file.write("\n\n# Move drawing to the center of the canvas\nfor i in app.group:\n\ti.left+=200-width/2\n\ti.top+=200-height/2")
    if generate_rainbow:
        file.write("\n\n\ndef onStep():\n\tfor i in app.group:\n\t\ti.fill=rgb(*hsv_to_rgb(app.hue,1,255))\n\tapp.hue+=app.hueStep\n\tif app.hue>1:\n\t\tapp.hue=0")

print(f"Rasterized image saved to {file_name}")
