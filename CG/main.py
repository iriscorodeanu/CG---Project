import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.affinity import rotate
from shapely.ops import unary_union
import random


# this function will generate random rectangles with their varying sizes, positions, and orientationss
def generate_random_rectangles(num_rects, x_range, y_range, width_range, height_range, allow_rotation=False):
    """
    -> generates random rectangles within specified size and position ranges.
    -> optionally applies random rotation to some rectangles (for a more complex approach).
    """
    rectangles = []
    for _ in range(num_rects):

        # randomly determine position and size for the rectangles
        x = random.uniform(*x_range)
        y = random.uniform(*y_range)
        width = random.uniform(*width_range)
        height = random.uniform(*height_range)

        # creates a rectangle polygon
        rect = Polygon([
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ])

        # optionally apply random rotation for complexity
        if allow_rotation:
            angle = random.uniform(0, 360)
            rect = rotate(rect, angle, origin='centroid')

        rectangles.append(rect)
    return rectangles


# predefined rectangles for a "non-randomized" mode - optional
def predefined_rectangles():
    """
    -> returns a fixeed set of rectangles for testing or debugging,, the number of rectangles is fixed.
    """
    return [
        Polygon([(5, 5), (20, 5), (20, 15), (5, 15)]),  # rectangle 1
        Polygon([(25, 25), (40, 25), (40, 35), (25, 35)]),  # rectangle 2
        Polygon([(10, 30), (30, 30), (30, 50), (10, 50)])  # rectangle 3
        # more can be added
    ]


# function to create a large rectangle that covers all given rectangles - "WORST CASE SCENARIO"
def create_covering_rectangle(rectangles):
    """
    -> creates a large rectangle that fully covers all the given rectangles.
    -> adds a small padding around the bounding box.
    """
    min_x = min(rect.bounds[0] for rect in rectangles) - 5  # leftmost X coordinate with padding
    min_y = min(rect.bounds[1] for rect in rectangles) - 5  # lowest Y coordinate with padding
    max_x = max(rect.bounds[2] for rect in rectangles) + 5  # rightmost X coordinate with padding
    max_y = max(rect.bounds[3] for rect in rectangles) + 5  # highest Y coordinate with padding

    # return the covering rectangle as a Polygon
    return Polygon([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)])


# parameters for controlling the program's behavior
randomize = True  # can be toggled: True for random rectangles OR False for predefined ones
num_rects = 25# the number of random rectangles to generate - can be changed as you wish
x_range = (0, 50)  # range for the X-coordinate of rectangles
y_range = (0, 50)  # range for the Y-coordinate of rectangles
width_range = (3, 20)  # range for rectangle widths
height_range = (3, 15)  # range for rectangle heights
include_worst_case = random.choice([True, False])  # randomly decide if the worst-case scenario is included (the big rectangle) - can be modified

# generate rectangles based on the toggle
if randomize:
    rectangles = generate_random_rectangles(num_rects, x_range, y_range, width_range, height_range, allow_rotation=True)
else:
    rectangles = predefined_rectangles()

# add a large covering rectangle if the worst-case scenario is enabled
if include_worst_case:
    covering_rectangle = create_covering_rectangle(rectangles)
    rectangles.append(covering_rectangle)

# combine all rectangles into a single shape (union of all polygons)
combined_shape = unary_union(rectangles)

# Plot 1: Show all individual rectangles - first picture
fig1, ax1 = plt.subplots(figsize=(8, 8))
for rect in rectangles:
    x, y = rect.exterior.xy
    ax1.plot(x, y, color="blue", linewidth=1)  # plotting each rectangle in BLUE
ax1.set_title("Separate Rectangles")  # setting plot title
ax1.set_aspect('equal')  # ensuringg equal scaling for both axes

# Plot 2: Show the combined contour of all rectangles - second picture
fig2, ax2 = plt.subplots(figsize=(8, 8))
if combined_shape.geom_type == 'Polygon':  # Single polygon case
    combined_x, combined_y = combined_shape.exterior.xy
    ax2.plot(combined_x, combined_y, color="red", linewidth=2)  # Plot the combined contour in red
elif combined_shape.geom_type == 'MultiPolygon':  # Multiple polygons case
    for polygon in combined_shape.geoms:
        combined_x, combined_y = polygon.exterior.xy
        ax2.plot(combined_x, combined_y, color="red", linewidth=2)  # Plot each part of the contour
ax2.set_title("Combined Contour")  # Set plot title
ax2.set_aspect('equal')  # Ensure equal scaling for booth axes

# Display both plots,,
plt.show()
