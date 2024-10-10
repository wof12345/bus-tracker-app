import cv2
import pytesseract

# Load the pre-trained Haar Cascade for license plate detection
plate_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')


def detect_license_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, 1.1, 10)

    for x, y, w, h in plates:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        plate_region = frame[y : y + h, x : x + w]

        plate_text = pytesseract.image_to_string(plate_region, config='--psm 8')
        print('License Plate:', plate_text.strip())

        cv2.putText(
            frame,
            plate_text.strip(),
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (36, 255, 12),
            2,
        )

    return frame


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect and show the license plate
        frame_with_plate = detect_license_plate(frame)

        # Display the frame
        cv2.imshow('License Plate Detection', frame_with_plate)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()


# Path to the input video
video_path = 'path_to_your_video.mp4'

# Run the detection on the video
process_video(video_path)
