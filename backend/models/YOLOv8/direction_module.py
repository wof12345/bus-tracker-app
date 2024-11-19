import numpy as np


def update_vehicle_direction(
    car_id, current_position, vehicle_tracker={}, main_axis='y', entry='+'
):
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

    last_direction = (
        vehicle_tracker[car_id]['direction'][-1]
        if len(vehicle_tracker[car_id]['direction']) > 0
        else 0
    )

    direction = axis_based_direction(
        current_position, last_position, last_direction, main_axis, entry
    )
    # direction = vector_based_direction(
    #     current_position, last_position, last_direction, main_axis, entry
    # )

    vehicle_tracker[car_id]['last_position'] = current_position
    vehicle_tracker[car_id]['direction'].append(direction)

    return vehicle_tracker


def axis_based_direction(
    current_position, last_position, last_direction, main_axis='y', entry='+'
):
    direction = 'unknown'

    if main_axis == 'y':
        if entry == '+':
            if current_position[1] > last_position[1]:
                direction = 'coming'
            elif current_position[1] < last_position[1]:
                direction = 'going'
            else:
                direction = last_direction
    else:
        if entry == '+':
            if current_position[0] > last_position[0]:
                direction = 'coming'
            elif current_position[0] < last_position[0]:
                direction = 'going'
            else:
                direction = last_direction

    return direction


def vector_based_direction(
    current_position, last_position, last_direction, main_axis='y', entry='+'
):
    direction = 'unknown'
    displacement_vector = current_position - last_position

    if displacement_vector > 0:
        direction = 'coming'
    elif displacement_vector < 0:
        direction = 'going'
    else:
        direction = last_direction

    return direction
