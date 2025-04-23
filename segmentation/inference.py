from nnunet.inference.predict import predict_from_folder
import os
import numpy as np
import nibabel as nib
from flask import jsonify

def run_segmentation(input_image_path, output_mask_path, model_path):
    # Ensures the model path exists
    if not os.path.exists(model_path):
        return jsonify({"error": "Model path does not exist."}), 404

    # Runs the nnUNet model inference``
    try:
        predict_from_folder(
            model_folder=model_path,
            input_folder=input_image_path,
            output_folder=output_mask_path,
            folds=[0, 1, 2, 3, 4],  # Use all folds for ensemble predictions
            save_npz=False,
            num_threads_preprocessing=1,
            num_threads_nifti_save=1,
            trainer_class_name="nnUNetTrainerV2",
            overwrite_existing=True,
            mode="normal"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Load the generated mask
    mask_img = nib.load(output_mask_path)
    mask_data = mask_img.get_fdata()

    # Return the mask data as a response
    return jsonify({"mask_shape": mask_data.shape, "mask_path": output_mask_path}), 200