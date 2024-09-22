from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from starlette.requests import Request
import io


router = APIRouter()


@router.post('/process-frame')
async def process_frame(file: UploadFile = File(...)):
    # Read the incoming file as bytes
    contents = await file.read()
    np_array = np.frombuffer(contents, np.uint8)

    # Decode the image frame
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # Process the frame (e.g., object detection, OCR, etc.)
    # Example: Convert to grayscale and return (You can replace this with TensorFlow model or Tesseract for OCR)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Encode processed frame back to JPEG to send it back to the client
    _, buffer = cv2.imencode('.jpg', gray_frame)
    processed_bytes = buffer.tobytes()

    return StreamingResponse(io.BytesIO(processed_bytes), media_type='image/jpeg')
