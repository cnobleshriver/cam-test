import cv2
import serial
import struct
import time

arduino = serial.Serial('/dev/cu.usbmodem11101', 115200)

arduino.write(b'<90,90>')

def send_command(x=None, y=None, fire=False):
    if fire:
        arduino.write(struct.pack('BB', 255, 255))
    else:
        x = max(0, min(180, x))  
        y = max(80, min(110, y))
        arduino.write(struct.pack('BB', x, y))

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

frame_center_x = 1280 // 2
frame_center_y = 720 // 2

error_threshold = 10
scan_speed = 2
pan_pos = 90
pan_dir = 1
last_sent = time.time()

while True:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            error_x = frame_center_x - face_center_x
            error_y = frame_center_y - face_center_y

            if abs(error_x) > error_threshold or abs(error_y) > error_threshold:
                if time.time() - last_sent > 0.1:
                    send_command(x=error_x, y=error_y)
                    last_sent = time.time()
            break
    else:
        pan_pos += scan_speed * pan_dir
        if pan_pos > 150 or pan_pos < 30:
            pan_dir *= -1
            pan_pos = max(30, min(pan_pos, 150))

        if time.time() - last_sent > 0.1:
            send_command(x=pan_pos, y=90)
            last_sent = time.time()

    cv2.imshow('img', img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):
        send_command(fire=True)
        time.sleep(0.5)
    elif key == ord('q'):
        break

cap.release()
arduino.close()
