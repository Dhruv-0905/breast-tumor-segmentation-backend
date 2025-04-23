import unittest
from backend.preprocessing.preprocessor import normalize_intensity, extract_channels

class TestPreprocessing(unittest.TestCase):

    def test_normalize_intensity(self):
        # Test case for intensity normalization
        input_image = ...  # Add a sample input image
        expected_output = ...  # Add the expected output after normalization
        output_image = normalize_intensity(input_image)
        self.assertEqual(output_image, expected_output)

    def test_extract_channels(self):
        # Test case for channel extraction
        input_image = ...  # Add a sample input image
        expected_channels = ...  # Add the expected channels
        output_channels = extract_channels(input_image)
        self.assertEqual(output_channels, expected_channels)

if __name__ == '__main__':
    unittest.main()