from backend.services.vehicles import get_vehicle, update_vehicle


def update_vehicle_based_on_plate(plates):
    for plate in plates:
        if plate:
            vehicle = get_vehicle({'license': plates[plate]['license']})

            print(vehicle, 'found')

            if vehicle:
                update_vehicle({'status': 'Stopped', 'in_campus': True}, vehicle['_id'])
