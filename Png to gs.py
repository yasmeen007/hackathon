import os
import cv2
import matplotlib.pyplot as plt

# Print current working directory (for debugging)
print("Current working directory:", os.getcwd())

# Enable interactive mode (optional)
plt.ion()  # Makes the plot display non-blocking

# Function to convert an image to grayscale
def convert_to_grayscale(image_path, output_path=None):
    # Load the image
    image = cv2.imread(image_path)

    # Check if the image is loaded
    if image is None:
        print("Error: Unable to load image. Check the file path.")
        return
    else:
        print("Image loaded successfully!")

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image if output path is specified
    if output_path:
        success = cv2.imwrite(output_path, gray_image)
        if success:
            print(f"Grayscale image saved to {output_path}")
        else:
            print("Failed to save the grayscale image!")

    # Display the original and grayscale images
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original Image")

    plt.subplot(1, 2, 2)
    plt.imshow(gray_image, cmap='gray')
    plt.title("Grayscale Image")

    plt.show()

# Example usage with an absolute output path
image_path = r"C:\SIRIUS\CraterImage.png"  # Correctly formatted path
output_path = r"C:\SIRIUS\greyscale_imageeee2.jpg"          # Use an absolute output path
convert_to_grayscale(image_path, output_path)
