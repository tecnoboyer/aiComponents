import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os

def analyze_organization(image1_path, image2_path):
    """
    Analyzes the organization of a spot in two images and returns a percentage score.

    Args:
        image1_path: Path to the first image (reference - should be organized).
        image2_path: Path to the second image (to be evaluated).

    Returns:
        A percentage score (0-100) indicating the organization similarity, or None if an error occurs.
        Also returns a text explanation of the reasoning.
    """

    try:
        # 1. Image Loading and Preprocessing
        img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)  # Load in grayscale
        img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

        if img1 is None or img2 is None:
            return None, "Error: Could not load images."

        # Resize for consistency (important for SSIM)
        img1 = cv2.resize(img1, (500, 500))  # Example size, adjust as needed
        img2 = cv2.resize(img2, (500, 500))

        # 2. Structural Similarity Index (SSIM)
        ssim_score, diff = ssim(img1, img2, full=True)

        # 3. Heuristic-based Organization Analysis
        # Example heuristic: Count the number of edges (more edges might indicate more clutter)
        edges1 = cv2.Canny(img1, 100, 200)
        edges2 = cv2.Canny(img2, 100, 200)

        edge_count1 = np.sum(edges1 > 0)
        edge_count2 = np.sum(edges2 > 0)

        # Calculate a simple organization score based on edge count difference
        edge_diff = abs(edge_count1 - edge_count2)
        max_edge_count = max(edge_count1, edge_count2)
        organization_score = 100 - (edge_diff / max_edge_count) * 100

        # 4. Generate Explanation
        explanation = f"""
        The organization similarity between the two images is {organization_score:.2f}%.

        Analysis:
        - Reference image edge count: {edge_count1}
        - Evaluated image edge count: {edge_count2}
        - SSIM Score: {ssim_score:.4f}

        The evaluated image has {'more' if edge_count2 > edge_count1 else 'fewer'} edges than the reference image, which may indicate {'more clutter' if edge_count2 > edge_count1 else 'less clutter'}.
        """

        return organization_score, explanation

    except Exception as e:
        return None, f"An error occurred: {e}"


# Example usage:
image1_path = "organized_spot.jpg"  # Path to the organized image
image2_path = "less_organized_spot.jpg"  # Path to the image to evaluate

percentage, explanation = analyze_organization(image1_path, image2_path)

if percentage is not None:
    print(f"Organization Similarity: {percentage:.2f}%")
    print("Explanation:", explanation)
else:
    print(explanation)  # Print the error message