import unittest
from scipy.spatial import distance
from main import eye_aspect_ratio


class TestDrowsiness(unittest.TestCase):
    def test_eye_aspect_ratio(self):
        # Test case with points defining an eye
        eye = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
        expected_aspect_ratio = (distance.euclidean((2, 2), (6, 6)) + distance.euclidean((3, 3), (5, 5))) / (
                    2 * distance.euclidean((1, 1), (4, 4)))
        result = eye_aspect_ratio(eye)
        self.assertAlmostEqual(result, expected_aspect_ratio)

if __name__ == '__main__':
    unittest.main()