import ast
import cv2
import numpy as np
import pandas as pd
from uuid import uuid4


def draw_border(
    img,
    top_left,
    bottom_right,
    color=(0, 255, 0),
    thickness=10,
    line_length_x=200,
    line_length_y=200,
):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.line(img, (x1, y1), (x1, y1 + line_length_y), color, thickness)  # -- top-left
    cv2.line(img, (x1, y1), (x1 + line_length_x, y1), color, thickness)

    cv2.line(
        img, (x1, y2), (x1, y2 - line_length_y), color, thickness
    )  # -- bottom-left
    cv2.line(img, (x1, y2), (x1 + line_length_x, y2), color, thickness)

    cv2.line(img, (x2, y1), (x2 - line_length_x, y1), color, thickness)  # -- top-right
    cv2.line(img, (x2, y1), (x2, y1 + line_length_y), color, thickness)

    cv2.line(
        img, (x2, y2), (x2, y2 - line_length_y), color, thickness
    )  # -- bottom-right
    cv2.line(img, (x2, y2), (x2 - line_length_x, y2), color, thickness)

    return img


def visualize(
    csv_path='models/YOLOv8/test.csv',
    outputPath='models/YOLOv8/',
    video_path='',
    show_video_simulation=False,
):
    results = pd.read_csv(csv_path)

    output_id = uuid4()
    output_id = ''

    # load video
    cap = cv2.VideoCapture(video_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(
        f'{outputPath}out{output_id}.mp4', fourcc, fps, (width, height)
    )

    license_plate = {}
    for car_id in np.unique(results['car_id']):
        # Identify the max score and filter results accordingly
        max_score = np.amax(
            results[results['car_id'] == car_id]['license_number_score']
        )

        # Filter rows with both car_id and max score
        car_results = results[
            (results['car_id'] == car_id)
            & (results['license_number_score'] == max_score)
        ]

        if not car_results.empty:
            selected_result = car_results.iloc[0]
            license_plate[car_id] = {
                'license_crop': None,
                'license_plate_number': selected_result['license_number'],
                'direction': selected_result['car_direction'],
            }

            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                selected_result['frame_nmr'],
            )
            ret, frame = cap.read()

            try:
                x1, y1, x2, y2 = ast.literal_eval(
                    selected_result['license_plate_bbox']
                    .replace('[ ', '[')
                    .replace('   ', ' ')
                    .replace('  ', ' ')
                    .replace(' ', ',')
                )
                license_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]
                license_crop = cv2.resize(
                    license_crop, (int((x2 - x1) * 400 / (y2 - y1)), 400)
                )
                license_plate[car_id]['license_crop'] = license_crop

            except Exception as e:
                print(f'Error processing bounding box for car_id {car_id}: {e}')
                license_plate[car_id]['license_crop'] = None

        else:
            # Handle case when no license plate is found for car_id
            license_plate[car_id] = {
                'license_crop': None,
                'license_plate_number': None,
                'direction': selected_result['car_direction'],
                # Or any default value or error handling
            }
    frame_nmr = -1
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Process each frame and annotate cars and license plates
    ret = True
    while ret:
        ret, frame = cap.read()
        frame_nmr += 1
        if ret:
            df_ = results[results['frame_nmr'] == frame_nmr]
            for row_indx in range(len(df_)):
                try:
                    # Draw car bounding box
                    car_x1, car_y1, car_x2, car_y2 = ast.literal_eval(
                        df_.iloc[row_indx]['car_bbox']
                        .replace('[ ', '[')
                        .replace('   ', ' ')
                        .replace('  ', ' ')
                        .replace(' ', ',')
                    )
                    draw_border(
                        frame,
                        (int(car_x1), int(car_y1)),
                        (int(car_x2), int(car_y2)),
                        (0, 255, 0),
                        thickness=5,
                        line_length_x=200,
                        line_length_y=200,
                    )

                    # Retrieve and display the direction
                    direction_text = license_plate[df_.iloc[row_indx]['car_id']].get(
                        'direction', 'unknown'
                    )

                    cv2.putText(
                        frame,
                        f'Direction: {direction_text}',
                        (int(car_x1), int(car_y1) - 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )

                    # Draw license plate bounding box
                    x1, y1, x2, y2 = ast.literal_eval(
                        df_.iloc[row_indx]['license_plate_bbox']
                        .replace('[ ', '[')
                        .replace('   ', ' ')
                        .replace('  ', ' ')
                        .replace(' ', ',')
                    )
                    cv2.rectangle(
                        frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4
                    )

                    # Insert cropped license plate image and text
                    license_crop = license_plate[df_.iloc[row_indx]['car_id']].get(
                        'license_crop'
                    )
                    if license_crop is not None:
                        H, W, _ = license_crop.shape
                        frame[
                            int(car_y1) - H - 100 : int(car_y1) - 100,
                            int((car_x2 + car_x1 - W) / 2) : int(
                                (car_x2 + car_x1 + W) / 2
                            ),
                            :,
                        ] = license_crop
                        frame[
                            int(car_y1) - H - 400 : int(car_y1) - H - 100,
                            int((car_x2 + car_x1 - W) / 2) : int(
                                (car_x2 + car_x1 + W) / 2
                            ),
                            :,
                        ] = (255, 255, 255)
                        license_text = license_plate[df_.iloc[row_indx]['car_id']].get(
                            'license_plate_number', ''
                        )
                        (text_width, text_height), _ = cv2.getTextSize(
                            license_text,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            4.3,
                            17,
                        )
                        cv2.putText(
                            frame,
                            license_text,
                            (
                                int((car_x2 + car_x1 - text_width) / 2),
                                int(car_y1 - H - 250 + (text_height / 2)),
                            ),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            4.3,
                            (0, 0, 0),
                            17,
                        )

                except Exception as e:
                    print(f'Error drawing elements for frame {frame_nmr}: {e}')

            out.write(frame)
            frame = cv2.resize(frame, (1280, 720))
            if show_video_simulation:
                cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    out.release()
    cap.release()
    cv2.destroyAllWindows()
