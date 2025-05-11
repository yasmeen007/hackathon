import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = r'C:\Users\Zishan\Downloads\ch2_ohr_ncp_20240229T0921593215_b_brw_d18 (1).png'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Apply Gaussian Blur to smooth the image
blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Use Canny Edge Detection
edges = cv2.Canny(blurred, 40, 70)

# Find contoursk
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
contour_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 1)
path='CraterImage1.png'
cv2.imwrite(path,contour_image)
# Display the original image and the image with contours
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(image, cmap='gray')
plt.subplot(1, 2, 2)
plt.title('Contours')
plt.imshow(contour_image)
plt.show()