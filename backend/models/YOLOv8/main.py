import cv2


from fastapi import UploadFile
from ultralytics import YOLO
from packages.sort.sort import Sort, np
from models.YOLOv8.util import (
    get_car,
    read_license_plate,
    write_csv,
    update_vehicle_direction,
    is_plate_near_car,
)
from models.YOLOv8.visualize import visualize


import os


def save_video_file(file: UploadFile, folder: str = 'temp_videos'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, file.filename)

    with open(file_path, 'wb') as temp_file:
        content = file.file.read()
        temp_file.write(content)

    return file_path


def getLicensePlatesFromVideo(  # noqa: C901
    file: UploadFile,
    video_default_path='models/YOLOv8/sample.mp4',
    max_frames=20,
    classifier_path='classifiers/license_plate_detector.pt',
    model_path='models/YOLOv8/yolov8n.pt',
    generate_csv=False,
    output_path=None,
    show_video_simulation=False,
):
    results = {}
    vehicle_tracker = {}
    license_plate_texts = {}
    video_path = None

    if file:
        video_path = save_video_file(file, folder='temp_videos')

    mot_tracker = Sort()

    # load models
    coco_model = YOLO(model_path)
    license_plate_detector = YOLO(classifier_path)

    if not video_path:
        video_path = video_default_path

    # load video
    cap = cv2.VideoCapture(video_path)

    vehicles = [2, 3, 5, 7]

    stop_flag = False

    # read frames
    frame_nmr = -1
    ret = True

    # loop over frames
    while ret and not stop_flag:
        frame_nmr += 1
        ret, frame = cap.read()
        if ret and not stop_flag:
            if frame_nmr >= max_frames:
                stop_flag = False
                break

            frame += 1
            results[frame_nmr] = {}

            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection

                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            # Track vehicles
            track_ids = mot_tracker.update(np.asarray(detections_))

            # Detect license plates
            license_plates = license_plate_detector(frame)[0]
            license_plate_boxes = [
                license_plate[:4] + [license_plate[4]]
                for license_plate in license_plates.boxes.data.tolist()
            ]

            for xcar1, ycar1, xcar2, ycar2, car_id in track_ids:
                center_y = (ycar1 + ycar2) / 2
                center_x = (xcar1 + xcar2) / 2

                lx1, ly1, lx2, ly2 = [0, 0, 0, 0]

                vehicle_tracker = update_vehicle_direction(
                    car_id, (round(center_x), round(center_y)), vehicle_tracker
                )

                matched_plate = None
                for license_plate in license_plate_boxes:
                    x1, y1, x2, y2, score = license_plate

                    if is_plate_near_car(x1, y1, x2, y2, xcar1, ycar1, xcar2, ycar2):
                        matched_plate = license_plate
                        break

                license_plate_text = 'none'
                license_plate_text_score = 0

                if matched_plate:
                    lx1, ly1, lx2, ly2, score = matched_plate

                    # Crop the license plate
                    license_plate_crop = frame[
                        int(ly1) : int(ly2), int(lx1) : int(lx2), :
                    ]

                    # Process license plate
                    license_plate_crop_gray = cv2.cvtColor(
                        license_plate_crop, cv2.COLOR_BGR2GRAY
                    )

                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    license_plate_crop_gray = clahe.apply(license_plate_crop_gray)

                    # Apply adaptive thresholding
                    mean_intensity = np.mean(license_plate_crop_gray)
                    _, license_plate_crop_thresh = cv2.threshold(
                        license_plate_crop_gray,
                        mean_intensity - 20,
                        255,
                        cv2.THRESH_BINARY_INV,
                    )

                    # Read license plate number
                    license_plate_text, license_plate_text_score = read_license_plate(
                        license_plate_crop_thresh
                    )

                if license_plate_text is not None:
                    direction = (
                        vehicle_tracker[car_id]['direction'][-1]
                        if vehicle_tracker[car_id]['direction']
                        else 'unknown'
                    )

                    print(direction, 'testt')

                    license_plate_texts[car_id] = {
                        'license': license_plate_text,
                        'direction': vehicle_tracker[car_id]['direction'],
                        'id': car_id,
                    }

                    results[frame_nmr][car_id] = {
                        'car': {
                            'bbox': [xcar1, ycar1, xcar2, ycar2],
                            'direction': direction,
                        },
                        'license_plate': {
                            'bbox': [lx1, ly1, lx2, ly2],
                            'text': license_plate_text,
                            'bbox_score': score,
                            'text_score': license_plate_text_score,
                        },
                    }

    generate_csv = output_path or show_video_simulation

    if generate_csv:
        write_csv(results, 'models/YOLOv8/test.csv')

    if output_path:
        visualize(
            outputPath=output_path,
            video_path=video_path,
            show_video_simulation=show_video_simulation,
        )

    cap.release()
    # os.remove(video_path)

    return license_plate_texts
