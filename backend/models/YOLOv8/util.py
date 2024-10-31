import string
import easyocr
import numpy as np
import cv2
import re
from pytesseract import pytesseract


def update_vehicle_direction(car_id, current_position, vehicle_tracker={}):
    """
    Determine the direction of a vehicle based on displacement vectors.

    Args:
        car_id (int): The ID of the car.
        current_position (tuple): Current (x, y) position of the car.
        vehicle_tracker (dict): Dictionary to store vehicle tracking data.

    Returns:
        dict: Updated vehicle_tracker with direction information.
    """
    current_position = np.array(current_position)

    if car_id not in vehicle_tracker:
        vehicle_tracker[car_id] = {
            'last_position': current_position,
            'direction': [],
        }
        return vehicle_tracker

    last_position = vehicle_tracker[car_id]['last_position']

    displacement_vector = current_position - last_position

    print(
        displacement_vector,
        current_position[1],
        last_position[1],
        current_position[1] > last_position[1],
        current_position[1] < last_position[1],
        car_id,
    )

    if current_position[1] > last_position[1]:
        direction = 'coming'
    elif current_position[1] < last_position[1]:
        direction = 'going'
    else:
        direction = (
            vehicle_tracker[car_id]['direction'][-1]
            if len(vehicle_tracker[car_id]['direction']) > 0
            else 0
        )

    vehicle_tracker[car_id]['last_position'] = current_position
    vehicle_tracker[car_id]['direction'].append(direction)

    return vehicle_tracker


reader = easyocr.Reader(['en'], gpu=True)


char_to_int = {chr(i): i - 65 for i in range(65, 91)}


int_to_char = {i - 65: chr(i) for i in range(65, 91)}


def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write(
            '{},{},{},{},{},{},{},{}\n'.format(
                'frame_nmr',
                'car_id',
                'car_bbox',
                'license_plate_bbox',
                'license_plate_bbox_score',
                'license_number',
                'license_number_score',
                'car_direction',
            )
        )

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                if (
                    'car' in results[frame_nmr][car_id].keys()
                    and 'license_plate' in results[frame_nmr][car_id].keys()
                    and 'text' in results[frame_nmr][car_id]['license_plate'].keys()
                ):
                    f.write(
                        '{},{},{},{},{},{},{},{}\n'.format(
                            frame_nmr,
                            car_id,
                            '[{} {} {} {}]'.format(
                                results[frame_nmr][car_id]['car']['bbox'][0],
                                results[frame_nmr][car_id]['car']['bbox'][1],
                                results[frame_nmr][car_id]['car']['bbox'][2],
                                results[frame_nmr][car_id]['car']['bbox'][3],
                            ),
                            '[{} {} {} {}]'.format(
                                results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                results[frame_nmr][car_id]['license_plate']['bbox'][3],
                            ),
                            results[frame_nmr][car_id]['license_plate']['bbox_score'],
                            results[frame_nmr][car_id]['license_plate']['text'],
                            results[frame_nmr][car_id]['license_plate']['text_score'],
                            results[frame_nmr][car_id]['car']['direction'],
                        )
                    )
        f.close()


def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """
    if len(text) <= 3:
        return False

    for i, char in enumerate(text):
        if i in [0, 1, 4, 5, 6]:
            if char not in string.ascii_uppercase and char not in int_to_char.values():
                return False
        elif i in [2, 3]:
            if char not in string.digits and char not in char_to_int.keys():
                return False

    return True


def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    text = re.sub(r'[^a-zA-Z0-9]', '', text)
    license_plate_ = ''
    mapping = {
        0: int_to_char,
        1: int_to_char,
        4: int_to_char,
        5: int_to_char,
        6: int_to_char,
        2: char_to_int,
        3: char_to_int,
    }
    print(text, 'test')
    for index, letter in enumerate(text):
        if (
            index in mapping
            and index in mapping[index].keys()
            and letter in [0, 1, 2, 3, 4, 5, 6]
        ):
            license_plate_ += mapping[index][letter]
        else:
            license_plate_ += letter

    return license_plate_


def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    detections = reader.readtext(license_plate_crop)

    text = pytesseract.image_to_string(license_plate_crop)

    print(text)

    # print(detections, 'licesne')

    for detection in detections:
        bbox, text, score = detection

        text = text.upper().replace(' ', '')

        if license_complies_format(text):
            return format_license(text), score
            # return format_license(text), score

    return 'none', 0


def get_car(license_plate, vehicle_track_ids):
    """
    Retrieve the vehicle coordinates and ID based on the license plate coordinates.

    Args:
        license_plate (tuple): Tuple containing the coordinates of the license plate (x1, y1, x2, y2, score, class_id).
        vehicle_track_ids (list): List of vehicle track IDs and their corresponding coordinates.

    Returns:
        tuple: Tuple containing the vehicle coordinates (x1, y1, x2, y2) and ID.
    """
    x1, y1, x2, y2, score, class_id = license_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1


def is_plate_near_car(x1, y1, x2, y2, xcar1, ycar1, xcar2, ycar2):
    """
    Determine if a license plate bounding box (x1, y1, x2, y2) is within or near a car bounding box (xcar1, ycar1, xcar2, ycar2).

    Parameters:
        x1, y1, x2, y2 (float): Coordinates of the license plate bounding box.
        xcar1, ycar1, xcar2, ycar2 (float): Coordinates of the car bounding box.

    Returns:
        bool: True if the license plate is within or near the car's bounding box, False otherwise.
    """

    if x1 >= xcar1 and y1 >= ycar1 and x2 <= xcar2 and y2 <= ycar2:
        return True

    tolerance = 10
    if (
        x1 >= (xcar1 - tolerance)
        and y1 >= (ycar1 - tolerance)
        and x2 <= (xcar2 + tolerance)
        and y2 <= (ycar2 + tolerance)
    ):
        return True

    return False
