from models.YOLOv8.main import getLicensePlatesFromVideo
from fastapi import APIRouter


router = APIRouter()


@router.post('/extract-license-plates')
async def extract_license_plates():
    plates = getLicensePlatesFromVideo()

    return plates
