import unittest
from unittest import TestCase
from main import cv2
from main import Drowsiness, VideoStream, Database

drowsiness = Drowsiness()
vs = VideoStream()
db = Database()


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


# ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()
