import sys
import cv2  # For image manipulation
import dlib  # For face detection
import mysql.connector
import face_recognition
from playsound import playsound  # For wav sound
from scipy.spatial import distance
from datetime import datetime  # For time
from threading import Thread

ID = 0


class VideoStream:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def stop(self):
        self.cap.release()

    def read_frame(self):
        ret, frame = self.cap.read()
        return ret, frame


# ----------------------------------------------------------------------------------------------------------------------

class Database:
    my_data_base = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="drowsiness"
    )

    # This function will create a cursor || Turki
    def database_connection(self):
        try:
            cursor = self.my_data_base.cursor()
            return cursor
        except Exception as e:
            print("Error in Database: ", e)

    # This function will convert image to binary to stored in Database  || Turki
    def convert_image_to_binary(self, image):
        try:
            with open(image, 'rb') as file:  # rb = read as binary
                binary_data = file.read()
            return binary_data
        except Exception as e:
            print("Error in convert image to binary: ", e)

    def insert_to_database(self, cursor, image, timestamp):

        # Insert the detection to Database
        pic = self.convert_image_to_binary(image)
        cursor.execute("INSERT INTO detection VALUES (%s, %s, %s, %s)", ('', ID, pic, timestamp))
        self.my_data_base.commit()


# ----------------------------------------------------------------------------------------------------------------------
class FaceRecognition:
    # Recogintion
    # This is dictionary
    driver_faces = {
        'Turki.jpg': 'Turki',
        'Amer.jpg': 'Amer'
    }

    # Resource1: https://www.analyticsvidhya.com/blog/2022/04/face-recognition-system-using-python/
    # Resource2: https://github.com/ageitgey/face_recognition
    # Turki & Amer
    def knowing_driver(self):
        # This is list
        encoding = []
        names = []
        for path, name in self.driver_faces.items():
            # To find the face location
            picture = face_recognition.load_image_file(path)
            # Convert image into encoding
            encode = face_recognition.face_encodings(picture)[0]
            encoding.append(encode)
            names.append(name)
        return encoding, names

    def encodingFace(self, gray, face_encodings, face_names):

        # Convert image into encoding
        location = face_recognition.face_locations(gray)
        encode = face_recognition.face_encodings(gray, location)

        for encoding in encode:
            compare = face_recognition.compare_faces(face_encodings, encoding)
            name = "Unknown"

            if True in compare:
                first_match_index = compare.index(True)
                name = face_names[first_match_index]

                print(f"Detected {name}")
                if name == "Turki":
                    global ID
                    ID = 100
                elif name == "Amer":
                    ID = 101
                break

        if name != "Unknown":
            return True
        else:
            playsound("Sounds/no_name.wav")
            sys.exit()


# ----------------------------------------------------------------------------------------------------------------------

class Drowsiness:

    def __init__(self):
        # We will use Dlib’s pre-trained face detector for this task.
        self.detector = dlib.get_frontal_face_detector()
        # 2. الدخول إلى الكاميرا ووضع علامة على المعالم من ملف (.dat) للتنبؤ بموقع الأذن والعينين.
        self.predictor = dlib.shape_predictor("Dataset/shape_predictor_68_face_landmarks.dat")
        self.alarm_path = "Sounds/alarm.wav"

        # For drowsiness detection
        self.EYE_EAR_THRESHOLD = 0.30
        self.EYE_EAR_CONSEC_FRAMES = 20
        self.count = 0
        self.alarm_statu = False

    # This function to calculate the distance between landmarks on the opposite sides of the eyes. || Turki
    @staticmethod
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

    def landmarks(self, gray, frame):

        # Will return a list of rectangles representing the detected faces.
        faces = self.detector(gray)

        # Draw a rectangles around the image.
        for face in faces:
            x1 = face.left()
            x2 = face.right()
            y1 = face.top()
            y2 = face.bottom()

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            landmarks = self.predictor(gray, face)

            landmarks = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)]

            # Calculate eye aspect ratio (EAR)
            RE = landmarks[36:42]  # Right Eye
            LE = landmarks[42:48]  # Left Eye
            EAR = (self.eye_aspect_ratio(LE) + self.eye_aspect_ratio(RE)) / 2.0  # Ex. 0.60 / 2 = 0.3072386179930159
            return EAR


# ----------------------------------------------------------------------------------------------------------------------

def main():  # Turki & Amer

    db = Database()
    fr = FaceRecognition()
    vs1 = VideoStream()

    cursor = db.database_connection()

    # Intro Sound
    playsound("Sounds/Intro.wav")

    # Part1: Recognition the driver face.
    face_encodings, face_names = fr.knowing_driver()


    while True:
        try:
            ret, frame = vs1.read_frame()
            if not ret:
                break

            # Convert the frame to grayscale
            gray = frame[:, :, ::-1]
            stop = fr.encodingFace(gray, face_encodings, face_names)
            if stop == True:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exit...")
                break

        except Exception as e:
            playsound("Sounds/face.wav")
            print("Error in detection: ", e)

    # # Here will close all windows
    vs1.stop()
    cv2.destroyAllWindows()
    playsound("Sounds/ok.wav")

    # Part2: Drowsiness Detection process.
    # Start webcam
    vs2 = VideoStream()
    db2 = Database()
    dr = Drowsiness()
    # To read every frame
    while True:
        try:
            ret, frame = vs2.read_frame()
            if not ret:
                break  # Exit if video stream ended

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ear = dr.landmarks(gray, frame)

            # check EAR Thireshold with counter
            if ear < dr.EYE_EAR_THRESHOLD:
                dr.count += 1
                if dr.count >= dr.EYE_EAR_CONSEC_FRAMES:
                    if not dr.alarm_statu:
                        dr.alarm_statu = True
                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # To generate date
                        image = f"image_{timestamp}.jpg"
                        cv2.imwrite(image, frame)
                        Thread(target=playsound, args=(dr.alarm_path,)).start()  # To run a thread for alarm
                        print("Drowsiness detected!")
                        print(dr.count)
                        db2.insert_to_database(cursor, image, timestamp)

            else:
                dr.count = 0
                dr.alarm_statu = False


            cv2.putText(frame, f"EAR: {ear:.2f}", (20, 20),
                        cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)
            # To output the frame
            cv2.imshow("Frame", frame)

            # if the user insert 'q' the webcam close
            if cv2.waitKey(1) & 0xFF == ord("x"):
                break

        except Exception as e:
            playsound("Sounds/running.wav")
            print("Error in detection: ", e)

    # Here will close all windows
    vs2.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()