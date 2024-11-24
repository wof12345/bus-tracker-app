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


router = APIRouter()

clients: List[WebSocket] = []

active_client_sessions = {}

timer = {}

simulationDetails = {}


def convert_object_ids_to_str(data):
    """
    Recursively converts all ObjectId instances in a nested dictionary or list to strings.

    Args:
        data (dict | list): The dictionary or list to process.

    Returns:
        dict | list: The processed dictionary or list with ObjectIds converted to strings.
    """
    if isinstance(data, dict):
        return {
            key: convert_object_ids_to_str(value)
            if isinstance(value, (dict, list))
            else str(value)
            if isinstance(value, ObjectId)
            else value
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [convert_object_ids_to_str(item) for item in data]
    else:
        return data


def simulateBus(id):
    vehicle_col = database['vehicles']
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


async def broadCastLiveData(vehicle_id):
    try:
        vehicle = simulateBus(vehicle_id)

        for client in clients:
            await client.send_text(json.dumps(vehicle))

    except Exception as e:
        print('error', e)


def call_async_broadCastLiveData(vehicle_id):
    run(broadCastLiveData(vehicle_id))


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            vehicle = json.loads(data)
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
                    )
                    timer[vehicle_id].start()

    except Exception as e:
        print('error', e)
        print(f"Connection origin: {websocket.headers.get('origin')}")
        clients.remove(websocket)
        if vehicle_id in active_client_sessions:
            active_client_sessions[vehicle_id].remove(websocket)
            if len(active_client_sessions[vehicle_id]) == 0:
                timer[vehicle_id].shutdown(wait=False)
                del timer[vehicle_id]
