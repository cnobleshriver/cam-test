import cv2
import serial
import time

arduino = serial.Serial('/dev/cu.usbmodem11101', 115200)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

frame_center_x = 1280 // 2
frame_center_y = 720 // 2

error_threshold = 25
scan_speed = 2

while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            error_x = frame_center_x - face_center_x
            error_y = frame_center_y - face_center_y

            if abs(error_x) > error_threshold or abs(error_y) > error_threshold:
                arduino.write(f'<{error_x},{error_y}>'.encode())
            # else:
            #     arduino.write(b'fire>')
            break

    # Display
    cv2.imshow('img', img)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):
        arduino.write(b'fire>')
        time.sleep(0.5)
    elif key == ord('q'):
        break

cap.release()
arduino.close()