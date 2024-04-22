import cv2  # For image manipulation
import dlib  # For face detection
import mysql.connector
import face_recognition
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
EYE_EAR_CONSEC_FRAMES = 30

my_data_base = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="drowsiness"
)


# ----------------------------------------------------------------------------------------------------------------------
# This function will create a cursor || Turki
def database_connection():
    try:
        cursor = my_data_base.cursor()
        return cursor
    except Exception as e:
        print("Error in Database: ", e)


# ----------------------------------------------------------------------------------------------------------------------
# Resource: https://www.analyticsvidhya.com/blog/2022/04/face-recognition-system-using-python/

# Definition of driver's names || Amer
driver_names = ['Amer', 'Turki']

# Load images and create encodings for the known faces of the employees
encoding_faces = []
for face in driver_names:
    # make each name as image.jpg
    face_image = f'{face}.jpg'
    # To find the face location
    picture = face_recognition.load_image_file(face_image)
    # To convert an image from one color space to another
    pic = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)

    # Convert image into encoding
    encode = face_recognition.face_encodings(pic)[0]
    encoding_faces.append(encode)


def knowing_driver(detection_image):    # Amer
    # Load the detection image and convert it
    driver = face_recognition.load_image_file(detection_image)
    test = cv2.cvtColor(driver, cv2.COLOR_BGR2RGB)

    # Try to find face encodings in the detection image
    test_encode = face_recognition.face_encodings(test)
    if not test_encode:
        return "No faces found in the image."

    test_encoding = test_encode[0]

    # Compare faces and find a match
    compare = face_recognition.compare_faces(encoding_faces, test_encoding)
    if True in compare:
        first_match_index = compare.index(True)
        return driver_names[first_match_index]
    else:
        return "No match found."


# ----------------------------------------------------------------------------------------------------------------------
# This function to calculate the distance between landmarks on the opposite sides of the eyes. || Turki
def eye_aspect_ratio(eye):
    try:
        dis1 = distance.euclidean(eye[1], eye[5])
        # print(dis1) Ex. (9.0 - 11.0)
        dis2 = distance.euclidean(eye[2], eye[4])
        # print(dis2) Ex. (9.0 - 11.0)
        dis3 = distance.euclidean(eye[0], eye[3])
        # print(dis3) Ex. 30.01666203960727
        EAR = (dis1 + dis2) / (2.0 * dis3)
        # print(EAR) || Ex. 0.3892341510100462
        return EAR
    except Exception as e:
        print("Error in EAR method: ", e)


# ----------------------------------------------------------------------------------------------------------------------
# This function will convert image to binary to stored in Database  || Turki
def convert_image_to_binary(image):
    try:
        with open(image, 'rb') as file:  # rb = read as binary
            binary_data = file.read()
        return binary_data
    except Exception as e:
        print("Error in convert image to binary: ", e)


def main():     # Turki & Amer
    cursor = database_connection()
    # Start webcam
    cap = cv2.VideoCapture(0)  # 0 To start witxh first webcam

    count = 0
    alarm_path = "C://Users/taroo/PycharmProjects/pythonProject6/alarm.wav"
    alarm_statu = False

    # To read every frame
    while True:
        try:
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

                            # Example usage:
                            detection_image = image
                            driver_name = knowing_driver(detection_image)
                            print(driver_name)

                            if driver_name == "Turki":
                                id = 100
                            elif driver_name == "Amer":
                                id = 101
                            else:
                                id = 0

                            # To get the last value in the Detection table
                            query = "SELECT DetectionID FROM detection ORDER BY DetectionID DESC LIMIT 1"
                            cursor.execute(query)
                            result = cursor.fetchone()
                            value = int(result[0])
                            value += 1

                            # Insert the detection to Database
                            pic = convert_image_to_binary(image)
                            cursor.execute("INSERT INTO detection VALUES (%s, %s, %s, %s)", (value, id, pic, timestamp))
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

        except Exception as e:
            print("Error in detection: ", e)

    # Here will close all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
