import cv2  # For image manipulation
import dlib  # For face detection
import mysql.connector
from playsound import playsound  # For wav sound
from scipy.spatial import distance
from datetime import datetime  # For time
from threading import Thread

# We will use Dlib’s pre-trained face detector for this task.
detector = dlib.get_frontal_face_detector()

# 2. الدخول إلى الكاميرا ووضع علامة على المعالم من ملف (.dat) للتنبؤ بموقع الأذن والعينين.
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# For drowsiness detection
EYE_EAR_THRESHOLD = 0.25
EYE_EAR_CONSEC_FRAMES = 20

my_data_base = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="drowsiness"
    )
cursor = my_data_base.cursor()

# This function to calculate the distance between landmarks on the opposite sides of the eyes.
def eye_aspect_ratio(eye):
    dis1 = distance.euclidean(eye[1], eye[5])
    # print(dis1) Ex. (9.0 - 11.0)
    dis2 = distance.euclidean(eye[2], eye[4])
    # print(dis2) Ex. (9.0 - 11.0)
    dis3 = distance.euclidean(eye[0], eye[3])
    # print(dis3) Ex. 30.01666203960727
    EAR = (dis1 + dis2) / (2.0 * dis3)
    # print(EAR) || Ex. 0.3892341510100462
    return EAR


def convert_image_to_binary(image):
    with open(image, 'rb') as file:     # rb = read as binary
        binary_data = file.read()
    return binary_data


# Start webcam
cap = cv2.VideoCapture(0)  # 0 To start witxh first webcam

count = 0
alarm_path = "C://Users/taroo/PycharmProjects/pythonProject6/alarm.wav"
alarm_statu = False

# To read every frame
while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit if video stream ended

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Will return a list of rectangles representing the detected faces.
    faces = detector(gray)

    # Draw a rectangles around the image.
    for face in faces:
        x1 = face.left()
        x2 = face.right()
        y1 = face.top()
        y2 = face.bottom()

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        landmarks = predictor(gray, face)

        landmarks = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)]

        # Calculate eye aspect ratio (EAR)
        RE = landmarks[36:42]  # Right Eye
        LE = landmarks[42:48]  # Left Eye
        EAR = (eye_aspect_ratio(LE) + eye_aspect_ratio(RE)) / 2.0  # Ex. 0.60 / 2 = 0.3072386179930159
        # print(EAR)

        # check EAR Thireshold with counter
        if EAR < EYE_EAR_THRESHOLD:
            count += 1
            if count >= EYE_EAR_CONSEC_FRAMES:
                if not alarm_statu:
                    alarm_statu = True
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # To generate date
                    image = f"image_{timestamp}.jpg"
                    cv2.imwrite(image, frame)
                    Thread(target=playsound, args=(alarm_path,)).start()  # To run a thread for alarm
                    # playsound(alarm_path)
                    print("Drowsiness detected!")

                    pic=convert_image_to_binary(image)
                    cursor.execute("INSERT INTO detection VALUES (%s, %s, %s, %s)", ('1', '100', pic, timestamp))
                    cursor.execute("INSERT INTO report VALUES (1, 1)")
                    my_data_base.commit()

                    print(count)

                # cv2.putText(frame, "WARNING!", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)

        else:
            count = 0
            alarm_statu = False

        cv2.putText(frame, f"EAR: {EAR:.2f}", (20, 20),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)
        # To output the frame
        cv2.imshow("Frame", frame)

    # if the user insert 'q' the webcam close
    if cv2.waitKey(1) & 0xFF == ord("x"):
        break

# Here will close all windows
cap.release()
cv2.destroyAllWindows()