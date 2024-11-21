from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
from backend.database import database
from bson import ObjectId

router = APIRouter()

clients: List[WebSocket] = []


def simulateBus(id, index):
    collection = database['vehicles']
    vehicle = collection.find_one({'_id': ObjectId(id)})

    if not vehicle['assigned_route']:
        return 'Vehicle has no route'


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:
            print('ws tick')
            data = await websocket.receive_text()
            # Broadcast to all connected clients
            for client in clients:
                await client.send_text(data)
    except Exception as e:
        print(f"Connection origin: {websocket.headers.get('origin')}")
        clients.remove(websocket)
