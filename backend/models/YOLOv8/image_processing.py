import cv2
import numpy as np
from models.YOLOv8.license_plate_formats import is_valid_liicense_plate
from models.YOLOv8.util import read_license_plate


def process_image(image):
    processed_image = image

    image = clahe_and_grayscaled(image)

    image = otsu_threshold(image)

    image = dilation(image)

    image = erosion(image)

    processed_image = image

    return processed_image


def heuristic_based_processing(
    image, text, iteration=0, max_retries=40, base_threshold=50
):  # beta
    processed_image = image

    if iteration >= max_retries:
        return processed_image

    image = clahe_and_grayscaled(image)

    image = threshold(image, threshold=base_threshold)

    image = dilation(image)

    image = erosion(image)

    text, score = read_license_plate(image)

    if not is_valid_liicense_plate(text):
        if iteration == max_retries - 1:
            image = heuristic_based_processing(
                image,
                text,
                iteration=iteration + 1,
                max_retries=max_retries,
                base_threshold=base_threshold + 1,
            )
        else:
            image = adaptive_threshold(image)

    processed_image = image

    return image


def otsu_threshold(image):
    _, threshold = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return threshold


def adaptive_threshold(image):
    threshold = cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2,
    )

    return threshold


def threshold(image, mean_intensity=False, intensity=0):
    threshold = image

    if mean_intensity:
        mean_intensity = np.mean(image)
        _, threshold = cv2.threshold(
            image,
            mean_intensity + (intensity),
            255,
            cv2.THRESH_BINARY_INV,
        )
    else:
        _, threshold = cv2.threshold(
            image,
            72 if intensity == 0 else intensity,
            255,
            cv2.THRESH_BINARY_INV,
        )

    return threshold


def clahe_and_grayscaled(image):
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe_applied = clahe.apply(gray_scale)

    return clahe_applied


def erosion(image, kernal_size=(3, 3), iterations=1):
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, kernal_size)
    dilated = cv2.dilate(image, kernal, iterations)

    return dilated


def dilation(image, kernal_size=(3, 3), iterations=1):
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT, kernal_size)
    eroded = cv2.erode(image, kernal, iterations)

    return eroded


# trial and error methods
# kernel = np.ones((3, 3), np.uint8)
# cleaned_thresh = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)

# Apply erosion to reduce character thickness
# kernel = np.ones((3, 3), np.uint8)
# eroded_image = cv2.erode(threshold, kernel, iterations=1)

# equ = cv2.equalizeHist(threshold)

# kernel = np.ones((2, 2), np.uint8)
# equ = cv2.morphologyEx(equ, cv2.MORPH_OPEN, kernel)
# equ = cv2.morphologyEx(equ, cv2.MORPH_CLOSE, kernel)

# th2 = 50
# equ[equ >= th2] = 255
# equ[equ < th2] = 0

# blur = cv2.GaussianBlur(equ, (7, 7), 1)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# clean = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel, iterations=1)

# horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
# detect_horizontal = cv2.morphologyEx(
#     clean, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
# )
# clean[detect_horizontal > 0] = 0  # Mask horizontal lines

# vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15))
# detect_vertical = cv2.morphologyEx(
#     clean, cv2.MORPH_OPEN, vertical_kernel, iterations=2
# )
# clean[detect_vertical > 0] = 250
