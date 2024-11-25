from models.YOLOv8.main import getLicensePlatesFromVideo
from fastapi import APIRouter
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Optional
from backend.services.license_detection import update_vehicle_based_on_plate
from backend.models.vehicle import Vehicle


router = APIRouter()

VIDEO_MIME_TYPES = {
    'video/mp4',
    'video/avi',
    'video/mpeg',
    'video/x-msvideo',
    'video/webm',
}


@router.post('/extract-license-plates', response_model=list[Vehicle])
def extract_license_plates(
    file: UploadFile = File(...),
    generate_csv: Optional[bool] = True,
    output_video: Optional[bool] = True,
    show_video_simulation: Optional[bool] = True,
    output_path: Optional[str] = None,
    max_frames: Optional[int] = 100,
):
    # In a real-world scenerio the video will be streamed either from the camera directly or through an intermediary platform based on the camera's specs. This just simulates the video.
    if file.content_type not in VIDEO_MIME_TYPES:
        raise HTTPException(
            status_code=400, detail='Invalid file type. Please upload a video.'
        )

    generate_csv = True
    if output_video:
        output_path = 'models/YOLOv8/'

    plates = getLicensePlatesFromVideo(
        file=file,
        max_frames=max_frames,
        generate_csv=generate_csv,
        output_path=output_path,
        show_video_simulation=show_video_simulation,
    )

    vehicle_with_plates = update_vehicle_based_on_plate(plates)

    return vehicle_with_plates
