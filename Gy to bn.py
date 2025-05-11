import cv2

# Load the grayscale image
grayscale_image = cv2.imread(r"C:\SIRIUS\greyscale_imageeee2.jpg", cv2.IMREAD_GRAYSCALE)

# Check if the image is loaded
if grayscale_image is None:
    print("Error: Grayscale image not found at 'C:\\SIRIUS\\greyscale_imageeee2.jpg'")
else:
    # Apply binary threshold (e.g., threshold value 127)
    threshold_value = 50
    _, binary_image = cv2.threshold(grayscale_image, threshold_value, 255, cv2.THRESH_BINARY)

    # Save the binary image
    output_path = r"C:\SIRIUS\binary_image_2.jpg"
    cv2.imwrite(output_path, binary_image)

    # Inform the user
    print(f"Binary image saved as '{output_path}'. You can open it manually to view the output.")

