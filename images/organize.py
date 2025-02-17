import openai
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import os

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

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

        # 3. OpenAI Chat Completion
        messages = [
            {"role": "system", "content": "You are an expert at analyzing the organization of spaces based on images."},
            {"role": "user", "content": f"""
                Analyze the organization of a spot shown in two images. The first image (reference) depicts the spot in an organized state. The second image shows the same spot and needs to be compared against the organized state.

                Consider factors like:
                - Number  of items: Are more items than the  first (reference) image?
                - Spacing and alignment: Is there consistent spacing and alignment in the second image as in the first (reference) image?
               

                Based on these factors, provide:
                1. A percentage score (0-100) representing the organization similarity between the two images. Higher score means more similar and organized.
                2. A concise explanation justifying the score. Refer to specific visual elements if possible.
                3. Number of items in each image.

                SSIM Score (Structural Similarity): {ssim_score:.4f} (This provides a quantitative starting point)
            """}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Correct model for chat completions
            messages=messages,  # Use the messages structure
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        explanation = response.choices[0].message['content'].strip()  # Access content correctly

        # Extract the percentage score (robustly)
        try:
            percentage_str = next((s for s in explanation.split() if s.endswith("%")), None)
            if percentage_str:
                percentage = float(percentage_str.replace("%", ""))
            else:  # Handle cases where the percentage is not explicitly in the explanation
                percentage = ssim_score * 100  # Fallback to SSIM if needed
        except (ValueError, AttributeError):  # Handle parsing errors
             percentage = ssim_score * 100 # Fallback to SSIM if needed


        return percentage, explanation

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