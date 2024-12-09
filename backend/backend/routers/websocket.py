from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
from backend.database import database
from bson import ObjectId
import json
from backend.utils.timer import RepeatedTimer
from apscheduler.schedulers.background import BackgroundScheduler
from asyncio import run
from backend.services.vehicles import update_vehicle, get_vehicle
from backend.services.routes import get_route
from datetime import datetime

router = APIRouter()

clients: List[WebSocket] = []

active_client_sessions = {}

timer = {}

simulationDetails = {}


def convert_object_ids_to_str(data):
    """
    Recursively converts all ObjectId and datetime instances in a nested dictionary or list to strings.

    Args:
        data (dict | list): The dictionary or list to process.

    Returns:
        dict | list: The processed dictionary or list with ObjectIds and datetimes converted to strings.
    """
    if isinstance(data, dict):
        return {
            key: convert_object_ids_to_str(value)
            if isinstance(value, (dict, list))
            else str(value)
            if isinstance(
                value, (ObjectId, datetime)
            )  # Convert ObjectId and datetime to string
            else value
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [convert_object_ids_to_str(item) for item in data]
    else:
        return str(data) if isinstance(data, (ObjectId, datetime)) else data


def get_and_update_vehicle(data):
    license = data['license']
    lat = data['lat']
    lng = data['lng']

    vehicle = get_vehicle({'license': license})

    if not vehicle:
        return {'detail': 'Vehicle not found'}

    current_coordinates = [lat, lng]
    update_vehicle({'current_coordinates': current_coordinates}, vehicle['_id'])


def simulateBus(id):
    vehicle = get_vehicle({'_id': ObjectId(id)})
    returnObject = {}

    if not vehicle:
        return {'detail': 'Vehicle not found'}

    if not vehicle['route']:
        return {'detail': 'Vehicle has no route'}

    route = get_route({'_id': ObjectId(vehicle['route']['_id'])})

    if not route:
        return {'detail': 'Route record not found'}

    lines = route['lines']
    vehicle_id = str(vehicle['_id'])

    returnObject = vehicle

    if vehicle_id not in simulationDetails or simulationDetails[vehicle_id] is None:
        simulationDetails[vehicle_id] = 0
    else:
        if 0 <= simulationDetails[vehicle_id] < len(lines):
            current_coordinates = lines[simulationDetails[vehicle_id]]
            returnObject['coordinates'] = current_coordinates

            update_vehicle(
                {'current_coordinates': current_coordinates, 'status': 'Running'},
                vehicle_id,
            )

            simulationDetails[vehicle_id] = simulationDetails[vehicle_id] + 1
        else:
            timer[vehicle_id].shutdown(wait=False)
            del timer[vehicle_id]
            simulationDetails[vehicle_id] = None
            returnObject['coordinates'] = None
            update_vehicle({'current_coordinates': [], 'status': 'Stopped'}, vehicle_id)

    # print(returnObject, simulationDetails)

    vehicle = convert_object_ids_to_str(returnObject)

    return vehicle


def getBusData(id):
    vehicle = get_vehicle({'_id': ObjectId(id)})
    returnObject = {}

    if not vehicle:
        return {'detail': 'Vehicle not found'}

    if not vehicle['route']:
        return {'detail': 'Vehicle has no route'}

    route = get_route({'_id': ObjectId(vehicle['route']['_id'])})

    if not route:
        return {'detail': 'Route record not found'}

    vehicle_id = str(vehicle['_id'])

    returnObject = vehicle

    vehicle_last_move = None
    last_coordinates = None
    current_coordinates = vehicle['current_coordinates']

    if 'last_coordinates' in vehicle:
        last_coordinates = vehicle['last_coordinates']

    returnObject['coordinates'] = current_coordinates

    current_date = datetime.now()
    if 'last_move' in vehicle:
        vehicle_last_move = vehicle['last_move']

    status = 'Stopped'

    if vehicle_last_move:
        difference = current_date - vehicle_last_move

        # print(difference, 'diff')

        if (
            abs(difference.total_seconds()) < 30
            and last_coordinates != current_coordinates
        ):
            status = 'Running'

    returnObject['coordinates'] = current_coordinates
    update_vehicle(
        {
            'status': status,
            'last_move': datetime.now(),
            'last_coordinates': current_coordinates,
        },
        vehicle_id,
    )

    vehicle = convert_object_ids_to_str(returnObject)

    return vehicle


async def broadCastLiveData(vehicle_id):
    try:
        vehicle = simulateBus(vehicle_id)
        # vehicle = getBusData(vehicle_id)

        # print(active_client_sessions)

        for client in active_client_sessions[vehicle_id]:
            await client.send_text(json.dumps(vehicle))

    except Exception as e:
        print('error', e)


def call_async_broadCastLiveData(vehicle_id):
    # print(timer)
    run(broadCastLiveData(vehicle_id))


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    vehicles = []

    try:
        while True:
            data = await websocket.receive_text()

            data = json.loads(data)

            if 'type' not in data:
                get_and_update_vehicle(data)
                return

            vehicles = data['buses']

            for vehicle in vehicles:
                if '_id' not in vehicle:
                    return {'detail': 'No details found'}

                vehicle_id = vehicle['_id']

                if vehicle_id not in active_client_sessions:
                    active_client_sessions[vehicle_id] = []
                    active_client_sessions[vehicle_id].append(websocket)
                else:
                    active_client_sessions[vehicle_id].append(websocket)

                if vehicle_id:
                    if vehicle_id not in timer:
                        timer[vehicle_id] = BackgroundScheduler()
                        timer[vehicle_id].add_job(
                            call_async_broadCastLiveData,
                            'interval',
                            seconds=1,
                            args=[vehicle_id],
                            max_instances=2,
                        )
                        timer[vehicle_id].start()

    except Exception as e:
        print('error', e)
        print(
            f"Connection origin: {websocket.headers.get('origin')}",
        )
        clients.remove(websocket)
        for vehicle in vehicles:
            if '_id' not in vehicle:
                return {'detail': 'No details found'}

            vehicle_id = vehicle['_id']

            if vehicle_id in active_client_sessions:
                active_client_sessions[vehicle_id].remove(websocket)

                if len(active_client_sessions[vehicle_id]) == 0:
                    timer[vehicle_id].shutdown(wait=False)

                    del timer[vehicle_id]
                    del active_client_sessions[vehicle_id]
