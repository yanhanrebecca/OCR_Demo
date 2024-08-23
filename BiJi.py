import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure

def extract_contours(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply binary thresholding
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_bounding_box(contours):
    x, y, w, h = cv2.boundingRect(np.vstack(contours))
    return x, y, w, h

def get_stroke_directions(contours):
    directions = []
    for contour in contours:
        if len(contour) > 1:
            # Fit line to contour points
            [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
            angle = np.arctan2(vy, vx) * 180 / np.pi
            directions.append(angle)
    return directions

def plot_contours(image, contours, title):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    for contour in contours:
        contour = contour.reshape(-1, 2)  # Reshape to (N, 2)
        plt.plot(contour[:, 0], contour[:, 1], marker='o')
    plt.show()

# Load images
image1 = cv2.imread('5.jpg')
image2 = cv2.imread('6.jpg')

# Extract contours
contours1 = extract_contours(image1)
contours2 = extract_contours(image2)

# Get bounding boxes
x1, y1, w1, h1 = get_bounding_box(contours1)
x2, y2, w2, h2 = get_bounding_box(contours2)

# Get stroke directions
directions1 = get_stroke_directions(contours1)
directions2 = get_stroke_directions(contours2)

# Print results
print(f"Character 1 Bounding Box: x={x1}, y={y1}, w={w1}, h={h1}")
print(f"Character 2 Bounding Box: x={x2}, y={y2}, w={w2}, h={h2}")
print(f"Character 1 Stroke Directions: {directions1}")
print(f"Character 2 Stroke Directions: {directions2}")

# Plot contours
plot_contours(image1, contours1, "Character 1 Contours")
plot_contours(image2, contours2, "Character 2 Contours")
