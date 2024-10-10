import cv2


from fastapi import UploadFile
from ultralytics import YOLO
from packages.sort.sort import Sort, np
from models.YOLOv8.util import get_car, read_license_plate, write_csv
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
    videoPath='models/YOLOv8/sample.mp4',
    max_frames=20,
    classifier_path='classifiers/license_plate_detector.pt',
    model_path='models/YOLOv8/yolov8n.pt',
    generate_csv=False,
    output_path=None,
):
    results = {}

    video_path = save_video_file(file, folder='temp_videos')

    mot_tracker = Sort()

    # load models
    coco_model = YOLO(model_path)
    license_plate_detector = YOLO(classifier_path)

    if not video_path:
        video_path = videoPath

    # load video
    cap = cv2.VideoCapture(video_path)

    vehicles = [2, 3, 5, 7]

    license_plate_texts = set()
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

            # detect vehicles
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

            # track vehicles
            track_ids = mot_tracker.update(np.asarray(detections_))

            # detect license plates
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                # assign license plate to car
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                if car_id != -1:
                    # crop license plate
                    license_plate_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]

                    # process license plate
                    license_plate_crop_gray = cv2.cvtColor(
                        license_plate_crop, cv2.COLOR_BGR2GRAY
                    )
                    _, license_plate_crop_thresh = cv2.threshold(
                        license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV
                    )

                    # read license plate number
                    license_plate_text, license_plate_text_score = read_license_plate(
                        license_plate_crop_thresh
                    )

                    if license_plate_text is not None:
                        license_plate_texts.add(license_plate_text)

                        results[frame_nmr][car_id] = {
                            'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                            'license_plate': {
                                'bbox': [x1, y1, x2, y2],
                                'text': license_plate_text,
                                'bbox_score': score,
                                'text_score': license_plate_text_score,
                            },
                        }
    cap.release()
    os.remove(video_path)

    if generate_csv:
        write_csv(results, 'models/YOLOv8/')

    if output_path:
        visualize(outputPath=output_path, video_path=video_path)

    return license_plate_texts
