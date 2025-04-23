import unittest
from backend.segmentation.inference import run_segmentation
from backend.models.nnunet_model import load_model

class TestSegmentation(unittest.TestCase):

    def setUp(self):
        self.model = load_model('path/to/model/checkpoint')
        self.test_image = 'path/to/test/image.nii.gz'

    def test_segmentation_output_shape(self):
        segmentation_mask = run_segmentation(self.model, self.test_image)
        self.assertEqual(segmentation_mask.shape, (1, 256, 256, 256), "Output shape is incorrect")

    def test_segmentation_values(self):
        segmentation_mask = run_segmentation(self.model, self.test_image)
        unique_values = set(segmentation_mask.flatten())
        self.assertTrue(all(value in [0, 1] for value in unique_values), "Segmentation mask contains invalid values")

if __name__ == '__main__':
    unittest.main()