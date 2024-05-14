import unittest
from unittest import TestCase
from project import Drowsiness, VideoStream, Database
from playsound import playsound
from project import cv2
import face_recognition

drowsiness = Drowsiness()
vs = VideoStream()
db = Database()

class TestDriverRecognition(unittest.TestCase):

    def test_knowing_driver(self):
        driver_faces = {
            'Turki.jpg': 'Turki',
            'Amer.jpg': 'Amer'
        }

        encoding = []
        names = []

        for path, name in driver_faces.items():
            picture = face_recognition.load_image_file(path)
            encode = face_recognition.face_encodings(picture)[0]
            encoding.append(encode)
            names.append(name)

        # Assertions
        self.assertEqual(len(encoding), 2)
        self.assertEqual(len(names), 2)

class FaceEncodingTest(unittest.TestCase):

    def setUp(self):
        self.gray = face_recognition.load_image_file("Amer.jpg")
        self.face_encodings = [
            face_recognition.face_encodings(face_recognition.load_image_file("Amer.jpg"))[0],
            face_recognition.face_encodings(face_recognition.load_image_file("Turki.jpg"))[0],

        ]
        self.face_names = ["Turki", "Amer"]

    def test_encodingFace(self):
        location = face_recognition.face_locations(self.gray)
        encode = face_recognition.face_encodings(self.gray, location)

    class TestDatabase(TestCase):  # Turki & Saad

     def test_database_connection(self):     # Saad
        cursor = db.database_connection()
        self.assertIsInstance(cursor, object, "This function must return an object of MySQLCursorAbstract.")

    def test_convert_image_to_binary(self):  # Turki
        image = f"Turki.jpg"
        result = db.convert_image_to_binary(image)
        self.assertIsInstance(result, bytes, "This function must return a bytes.")


# ----------------------------------------------------------------------
class TestDrowsiness(unittest.TestCase):  # Turki Baatta
    def test_eye_aspect_ratio(self):  # Turki Baatta
        # Error in EAR method:  Input vector should be 1-D.
        # eye = (0, 1, 2, 3, 4, 5)
        eye = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
        result = drowsiness.eye_aspect_ratio(eye)
        self.assertIsInstance(result, float, "This function must return a float number.")

    def test_landmarks(self):  # Turki Baatta
        frame = cv2.imread("Turki.jpg")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        result = drowsiness.landmarks(gray, frame)
        self.assertIsInstance(result, float, "The result must be float number!")


# ----------------------------------------------------------------------
class TestVideoStream(unittest.TestCase):  # Turki Baatta
    def test_stop(self):  # Turki Baatta
        result = vs.stop()
        self.assertIsNone(result, "This is NOT NONE")

    def test_read_frame(self):  # Turki Baatta
        result = vs.read_frame()
        self.assertIsInstance(result, tuple, "The function should return a tuple")


if __name__ == '__main__':
    unittest.main()