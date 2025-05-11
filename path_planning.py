import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def preprocess_image(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Apply a binary threshold to create a binary image
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    return binary_image

def find_obstacle_free_points(binary_image, num_points=10):
    free_points = np.argwhere(binary_image == 255) 
    chosen_points = free_points[np.random.choice(free_points.shape[0], num_points, replace=False)]
    return chosen_points

def objective_function(waypoints_flattened):
    waypoints = waypoints_flattened.reshape(-1, 2)
    # The objective is to minimize the total distance traveled
    total_distance = 0
    for i in range(len(waypoints) - 1):
        total_distance += np.linalg.norm(waypoints[i] - waypoints[i + 1])
    return total_distance

def constraint_function(waypoints_flattened, binary_image):
    waypoints = waypoints_flattened.reshape(-1, 2)
    for point in waypoints:
        x, y = int(point[0]), int(point[1])
        if x < 0 or y < 0 or x >= binary_image.shape[0] or y >= binary_image.shape[1] or binary_image[x, y] == 0:
            return -1  # Constraint violated
    return 0  # Constraint satisfied

def main():
    image_path = 'C:\SIRIUS\Figure_1.png'
    binary_image = preprocess_image(image_path)
    
    # Find ten obstacle-free points
    initial_waypoints = find_obstacle_free_points(binary_image, 10).flatten()

    # Define constraints
    constraints = {'type': 'ineq', 'fun': lambda w: constraint_function(w, binary_image)}

    # Define the optimization problem
    result = minimize(objective_function, initial_waypoints, constraints=constraints, method='SLSQP', options={'disp': True})

    # Extract the optimized waypoints
    optimized_waypoints = result.x.reshape(-1, 2)

    # Plot the binary image with the optimized path
    plt.imshow(binary_image, cmap='gray')
    plt.plot(optimized_waypoints[:, 1], optimized_waypoints[:, 0], 'r-')
    plt.scatter(optimized_waypoints[:, 1], optimized_waypoints[:, 0], c='blue', marker='o')
    plt.title('Path Planning with Optimized Waypoints')
    plt.show()

if __name__ == "__main__":
    main()
