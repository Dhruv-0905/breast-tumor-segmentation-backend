import nibabel as nib
import numpy as np
from skimage.transform import resize

def preprocess_nifti(nifti_path, target_shape=(128, 128, 128)):
    img = nib.load(nifti_path)
    data = img.get_fdata()

    # Normalize intensity
    data = (data - np.min(data)) / (np.max(data) - np.min(data))

    # Resize to target shape
    resized = resize(data, target_shape, mode='constant', preserve_range=True)

    # Save the preprocessed image
    new_img = nib.Nifti1Image(resized, affine=img.affine)
    preprocessed_path = nifti_path.replace("raw", "processed").replace(".nii", "_preprocessed.nii")
    nib.save(new_img, preprocessed_path)

    return preprocessed_path
