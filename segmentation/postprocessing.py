def refine_segmentation_mask(segmentation_mask, threshold=0.5, min_size=500, closing_disk_size=3):
    """
    Refines the segmentation mask using thresholding and morphological operations.
    
    Parameters:
    - segmentation_mask: The initial segmentation mask to refine. (should be a numpy array)
    - threshold: The threshold value for binarization.
    - min_size: The minimum size of objects to keep.
    - closing_disk_size: The disk size for the closing operation.
    
    Returns:
    - refined_mask: The refined segmentation mask (numpy array).
    """
    import numpy as np
    from skimage import morphology

    if not isinstance(segmentation_mask, np.ndarray):
        raise ValueError("segmentation_mask must be a numpy array")

    # Binarize the mask based on the threshold
    binary_mask = (segmentation_mask > threshold).astype(np.uint8)

    # Perform morphological operations to clean up the mask
    cleaned_mask = morphology.remove_small_objects(binary_mask, min_size=min_size)
    refined_mask = morphology.binary_closing(cleaned_mask, morphology.disk(closing_disk_size))

    return refined_mask

def postprocess_segmentation(segmentation_mask):
    """
    Post-processes the segmentation mask to enhance the results.
    
    Parameters:
    - segmentation_mask: The initial segmentation mask to post-process. (should be a numpy array)
    
    Returns:
    - final_mask: The final post-processed segmentation mask (numpy array).
    """
    # Apply thresholding and morphological operations
    final_mask = refine_segmentation_mask(segmentation_mask)
    
    return final_mask
