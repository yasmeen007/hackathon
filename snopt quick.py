import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Landing site coordinates (as a pixel reference)
LANDING_COORDINATES = (-85.24800, 31.20400)

# Preprocess the image (crop to zoomed area and binarize)
def preprocess_image(image_path, crop_area=(500, 1000)):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError("Image not found. Ensure the image path is correct.")
    
    # Crop the image to a specified area
    cropped_image = image[:crop_area[0], :crop_area[1]]  # Crop to 500m x 1000m simulation
    
    # Apply binary thresholding (threshold = 127 for crater detection)
    _, binary_image = cv2.threshold(cropped_image, 127, 255, cv2.THRESH_BINARY)
    return binary_image

# Find random free points (obstacle-free) and include landing point
def find_obstacle_free_points(binary_image, num_points=10):
    free_points = np.argwhere(binary_image == 255)  # Identify all obstacle-free points
    if free_points.shape[0] == 0:
        raise ValueError("No free points found. Check your binary image.")
    
    chosen_points = free_points[np.random.choice(free_points.shape[0], num_points - 1, replace=False)]
    landing_point = np.array([[binary_image.shape[0] // 2, binary_image.shape[1] // 2]])  # Placeholder landing pixel
    chosen_points = np.vstack((landing_point, chosen_points))  # Add landing point
    return chosen_points

# Objective function to minimize total distance
def objective_function(waypoints_flattened):
    waypoints = waypoints_flattened.reshape(-1, 2)
    total_distance = 0
    for i in range(len(waypoints) - 1):
        total_distance += np.linalg.norm(waypoints[i] - waypoints[i + 1])
    return total_distance

# Constraint to ensure waypoints are in free regions
def constraint_function(waypoints_flattened, binary_image):
    waypoints = waypoints_flattened.reshape(-1, 2)
    for point in waypoints:
        x, y = int(point[0]), int(point[1])
        if x < 0 or y < 0 or x >= binary_image.shape[0] or y >= binary_image.shape[1] or binary_image[x, y] == 0:
            return -1  # Constraint violated
    return 0  # Constraint satisfied

# Ensure a minimum distance between waypoints
def minimum_distance_constraint(waypoints_flattened, min_distance=100):
    waypoints = waypoints_flattened.reshape(-1, 2)
    for i in range(len(waypoints) - 1):
        if np.linalg.norm(waypoints[i] - waypoints[i + 1]) < min_distance:
            return -1  # Constraint violated
    return 0  # Constraint satisfied

def main():
    image_path = r"C:\SIRIUS\greyscale_imageeee2.jpg"  # Provide the correct image path
    binary_image = preprocess_image(image_path)

    # Find obstacle-free points, including landing site
    initial_waypoints = find_obstacle_free_points(binary_image, 10).flatten()

    # Define constraints
    constraints = [
        {'type': 'ineq', 'fun': lambda w: constraint_function(w, binary_image)},
        {'type': 'ineq', 'fun': lambda w: minimum_distance_constraint(w)}
    ]

    # Solve the optimization problem
    result = minimize(objective_function, initial_waypoints, constraints=constraints, method='SLSQP', options={'disp': True})

    # Extract optimized waypoints
    optimized_waypoints = result.x.reshape(-1, 2)

    # Plot the optimized path with waypoints and annotations
    plt.imshow(binary_image, cmap='gray')
    plt.plot(optimized_waypoints[:, 1], optimized_waypoints[:, 0], 'r-', linewidth=2)  # Path
    plt.scatter(optimized_waypoints[:, 1], optimized_waypoints[:, 0], c='blue', marker='o')  # Waypoints

    # Annotate waypoints with their number and distance
    for i, waypoint in enumerate(optimized_waypoints):
        plt.text(waypoint[1], waypoint[0], f'WP{i+1}', color='yellow', fontsize=8, ha='center', va='center')
        if i > 0:
            distance = np.linalg.norm(optimized_waypoints[i] - optimized_waypoints[i - 1])
            mid_point = (waypoint + optimized_waypoints[i - 1]) / 2
            plt.text(mid_point[1], mid_point[0], f'{distance:.2f}m', color='cyan', fontsize=6, ha='center')

    plt.title('Optimized Path with Annotated Waypoints and Distances')
    plt.show()

if __name__ == "__main__":
    main()
