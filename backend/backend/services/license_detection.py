from backend.services.vehicles import get_vehicle, update_vehicle


def update_vehicle_based_on_plate(plates):
    vehicle_with_plates = []

    for plate in plates:
        if plate:
            plate_obj = plates[plate]
            vehicle = get_vehicle({'license': plate_obj['license']})

            if vehicle:
                if plate_obj['direction'] == 'coming':
                    update_vehicle(
                        {'status': 'Stopped', 'in_campus': True}, vehicle['_id']
                    )
                elif plate_obj['direction'] == 'going':
                    update_vehicle(
                        {'status': 'Running', 'in_campus': False}, vehicle['_id']
                    )
                else:
                    update_vehicle(
                        {'status': 'Unknown', 'in_campus': False}, vehicle['_id']
                    )

                vehicle_with_plates.append(vehicle)

    return vehicle_with_plates
