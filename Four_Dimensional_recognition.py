import os
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scipy.spatial import distance

def calculate_min_distance(box1, box2):
    """Calculate the minimum distance between two bounding boxes."""
    # Coordinates for box1
    x1_min, y1_min = box1[0], box1[1]
    x1_max, y1_max = box1[0] + box1[2], box1[1] + box1[3]

    # Coordinates for box2
    x2_min, y2_min = box2[0], box2[1]
    x2_max, y2_max = box2[0] + box2[2], box2[1] + box2[3]

    # Compute distances between the closest points
    horizontal_dist = max(x1_min, x2_min) - min(x1_max, x2_max)
    vertical_dist = max(y1_min, y2_min) - min(y1_max, y2_max)

    # If boxes overlap in either axis, the distance is 0 for that axis
    horizontal_dist = max(0, horizontal_dist)
    vertical_dist = max(0, vertical_dist)

    return np.sqrt(horizontal_dist**2 + vertical_dist**2)

def annotate_and_plot_image(image_path, threshold_distance=50, save_path=None, font_size=12):
    try:
        # 1. Open image
        image = Image.open(image_path)

        # 2. Convert to grayscale
        gray_image = image.convert('L')
        image_array = np.array(gray_image)

        # Binarize the image
        _, binary_image = cv2.threshold(image_array, 128, 255, cv2.THRESH_BINARY_INV)

        # 3. Extract contours
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 4. Create a color image for annotations
        color_image = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)

        # Set the font for annotation
        font_path = 'D:\\Download\\SimHei.ttf'  # Windows font path
        prop = font_manager.FontProperties(fname=font_path, size=font_size)
        plt.rcParams['font.family'] = prop.get_name()

        # 5. Calculate distances between strokes and annotate
        bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
        connected_strokes = 0

        for i in range(len(contours)):
            for j in range(i + 1, len(contours)):
                box1 = bounding_boxes[i]
                box2 = bounding_boxes[j]

                # Calculate minimum distance between the two bounding boxes
                dist = calculate_min_distance(box1, box2)

                if dist < threshold_distance:
                    # Draw contours of connected strokes in different colors based on distance
                    color = (0, 0, 255) if dist < threshold_distance / 2 else (255, 0, 0)
                    cv2.drawContours(color_image, contours, i, color, 2)
                    cv2.drawContours(color_image, contours, j, color, 2)

                    # Calculate the centroid of contours
                    M1 = cv2.moments(contours[i])
                    M2 = cv2.moments(contours[j])

                    if M1['m00'] != 0 and M2['m00'] != 0:
                        c1_x = int(M1['m10'] / M1['m00'])
                        c1_y = int(M1['m01'] / M1['m00'])
                        c2_x = int(M2['m10'] / M2['m00'])
                        c2_y = int(M2['m01'] / M2['m00'])

                        # Draw circles at the centroids of connected strokes
                        cv2.circle(color_image, (c1_x, c1_y), 10, (0, 255, 0), 2)
                        cv2.circle(color_image, (c2_x, c2_y), 10, (0, 255, 0), 2)

                        # Draw a line connecting the centroids
                        cv2.line(color_image, (c1_x, c1_y), (c2_x, c2_y), (255, 255, 0), 2)

                        connected_strokes += 1

        # 6. Display and optionally save the image
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(f'Connected Strokes: {connected_strokes}', fontproperties=prop)
        plt.show()

        if save_path:
            # Save the annotated image
            annotated_image = Image.fromarray(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
            annotated_image.save(save_path)
            print(f"Annotated image saved to: {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_images_in_folder(folder_path, output_folder, threshold_distance=50, font_size=12):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            save_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_annotated.jpg")
            annotate_and_plot_image(image_path, threshold_distance, save_path, font_size)

# Usage example
folder_path = './result/Test/T'
output_folder = './result'
process_images_in_folder(folder_path, output_folder, threshold_distance=50, font_size=14)
