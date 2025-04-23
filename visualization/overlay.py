import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

def create_overlay_images(mri_path, mask_path, output_dir, alpha=0.4):
    os.makedirs(output_dir, exist_ok=True)

    mri_nii = nib.load(mri_path)
    mask_nii = nib.load(mask_path)

    mri_data = mri_nii.get_fdata()
    mask_data = mask_nii.get_fdata()

    mri_data = (mri_data - mri_data.min()) / (mri_data.max() - mri_data.min()) * 255
    mri_data = mri_data.astype(np.uint8)

    mask_data = (mask_data > 0).astype(np.uint8)

    mid_slice = mri_data.shape[2] // 2
    slice_range = range(mid_slice - 2, mid_slice + 3)

    for i in slice_range:
        mri_slice = mri_data[:, :, i]
        mask_slice = mask_data[:, :, i]

        overlay = cv2.cvtColor(mri_slice, cv2.COLOR_GRAY2BGR)
        overlay[mask_slice == 1] = [255, 0, 0]  # red overlay

        blended = cv2.addWeighted(cv2.cvtColor(mri_slice, cv2.COLOR_GRAY2BGR), 1 - alpha, overlay, alpha, 0)

        output_path = os.path.join(output_dir, f"slice_{i}.png")
        cv2.imwrite(output_path, blended)

    return output_dir
