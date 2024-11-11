from paddleocr import PaddleOCR
import re


reader = PaddleOCR(lang='en', gpu=True)


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
    if len(text) <= 3 or len(text) > 7:
        return False

    # for i, char in enumerate(text):
    #     if i in [0, 1, 4, 5, 6]:
    #         if char not in string.ascii_uppercase and char not in int_to_char.values():
    #             return False
    #     elif i in [2, 3]:
    #         if char not in string.digits and char not in char_to_int.keys():
    #             return False

    return True


def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """

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

    detections = reader.ocr(license_plate_crop)

    for line in detections:
        if not line:
            continue
        for word_info in line:
            text = word_info[1][0]
            confidence = word_info[1][1]

            text = text.upper().replace(' ', '')
            text = re.sub(r'[^a-zA-Z0-9]', '', text)
            if license_complies_format(text):
                # print(text, 'debugtesst')
                # return format_license(text), score
                return text, confidence

    return 'none', 0


def get_highest_average_direction(vehicle_tracker, car_id):
    direction_counts = {'unknown': 0, 'coming': 0, 'going': 0}
    total_counts = 0

    directions = vehicle_tracker[car_id]['direction']
    for direction in directions:
        if direction in direction_counts:
            direction_counts[direction] += 1
            total_counts += 1

    if total_counts == 0:
        return 'No directions recorded'

    averages = {k: v / total_counts for k, v in direction_counts.items()}

    highest_avg_direction = max(averages, key=averages.get)
    return [highest_avg_direction, averages[highest_avg_direction]]


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

    tolerance = 20
    if (
        x1 >= (xcar1 - tolerance)
        and y1 >= (ycar1 - tolerance)
        and x2 <= (xcar2 + tolerance)
        and y2 <= (ycar2 + tolerance)
    ):
        return True

    return False
