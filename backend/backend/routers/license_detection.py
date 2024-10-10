from models.YOLOv8.main import getLicensePlatesFromVideo
from fastapi import APIRouter
from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Optional


router = APIRouter()

VIDEO_MIME_TYPES = {
    'video/mp4',
    'video/avi',
    'video/mpeg',
    'video/x-msvideo',
    'video/webm',
}


@router.get('/extract-license-plates')
def extract_license_plates(
    file: UploadFile = File(...),
    generate_csv: Optional[bool] = False,
    output_path: Optional[str] = None,
):
    if file.content_type not in VIDEO_MIME_TYPES:
        raise HTTPException(
            status_code=400, detail='Invalid file type. Please upload a video.'
        )

    generate_csv = True
    output_path = 'models/YOLOv8/'

    plates = getLicensePlatesFromVideo(
        file=file, max_frames=50, generate_csv=generate_csv, output_path=output_path
    )

    return plates
