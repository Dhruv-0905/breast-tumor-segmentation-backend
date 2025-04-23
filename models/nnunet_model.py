from nnunet.inference import predict_from_folder
import os
import numpy as np
import nibabel as nib

class NnUNetModel:
    def __init__(self, model_folder: str):
        self.model_folder = model_folder
        self.model = self.load_model()

    def load_model(self):
        # Load the nnUNet model from the specified folder
        if not os.path.exists(self.model_folder):
            raise FileNotFoundError(f"Model folder {self.model_folder} does not exist.")
        return self.model_folder

    def predict(self, input_image_path: str) -> np.ndarray:
        # Run inference on the input image and return the segmentation mask
        if not os.path.exists(input_image_path):
            raise FileNotFoundError(f"Input image {input_image_path} does not exist.")
        
        # Use nnUNet's predict_from_folder function to get the segmentation
        predictions = predict_from_folder(self.model, input_image_path)
        return predictions

    def save_segmentation(self, segmentation: np.ndarray, output_path: str):
        # Save the segmentation mask as a NIfTI file
        img = nib.Nifti1Image(segmentation, affine=np.eye(4))
        nib.save(img, output_path)