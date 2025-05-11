import cv2
import numpy as np
import matplotlib.pyplot as plt

# Landing site coordinates
LANDING_COORDINATES = (-85.24800, 31.20400)

def preprocess_image(image_path, crop_area=(500, 1000), threshold_value=80):
    """
    Preprocess the input image: crop and convert to binary.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError("Image not found. Ensure the image path is correct.")

    cropped_image = image[:crop_area[0], :crop_area[1]]
    _, binary_image = cv2.threshold(cropped_image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_image

def find_safe_waypoints(binary_image, landing_pixel, num_points=10, step_distance=30):
    """
    Finds safe waypoints, ensuring points are in free (white) areas of the binary image.
    """
    height, width = binary_image.shape
    safe_waypoints = [landing_pixel]

    for _ in range(num_points - 1):
        found_safe_point = False
        for y in range(landing_pixel[0] - step_distance, landing_pixel[0] + step_distance + 1):
            for x in range(landing_pixel[1] - step_distance, landing_pixel[1] + step_distance + 1):
                if 0 <= x < width and 0 <= y < height and binary_image[y, x] == 255:
                    safe_waypoints.append((y, x))
                    landing_pixel = (y, x)
                    found_safe_point = True
                    break
            if found_safe_point:
                break
        if not found_safe_point:
            raise ValueError("Unable to find a safe waypoint. Check the binary image or adjust parameters.")

    return np.array(safe_waypoints)

def pixel_to_coordinates(pixel, binary_image, landing_coordinates=LANDING_COORDINATES):
    """
    Convert pixel coordinates to latitude and longitude.
    """
    image_height, image_width = binary_image.shape
    lat_range = 0.001  # Example scale for latitude
    lon_range = 0.001  # Example scale for longitude

    lat = landing_coordinates[0] + (pixel[0] / image_height) * lat_range
    lon = landing_coordinates[1] + (pixel[1] / image_width) * lon_range
    return lat, lon

def main():
    image_path = r"C:\SIRIUS\greyscale_imageeee2.jpg"
    binary_image = preprocess_image(image_path)

    initial_landing_pixel = (binary_image.shape[0] // 2, binary_image.shape[1] // 2)

    # Find waypoints
    safe_waypoints = find_safe_waypoints(binary_image, initial_landing_pixel, num_points=15, step_distance=20)

    lat_lon_waypoints = [pixel_to_coordinates(wp, binary_image) for wp in safe_waypoints]

    # Plot the path and label all waypoints
    plt.imshow(binary_image, cmap='gray')
    plt.plot(safe_waypoints[:, 1], safe_waypoints[:, 0], 'r-', linewidth=2)
    plt.scatter(safe_waypoints[:, 1], safe_waypoints[:, 0], c='blue', marker='o')

    for i, (waypoint, (lat, lon)) in enumerate(zip(safe_waypoints, lat_lon_waypoints)):
        plt.text(waypoint[1], waypoint[0], f'WP{i+1}', color='yellow', fontsize=8, ha='center', va='center')
        plt.text(waypoint[1], waypoint[0] + 10, f'Lat: {lat:.6f}\nLon: {lon:.6f}', color='cyan', fontsize=6, ha='center')

    plt.title('Optimized Path with Annotated Waypoints and Coordinates')
    plt.show()


if __name__ == "__main__":
    main()
