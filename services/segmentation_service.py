import os
import shutil
import traceback
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from config import settings
from preprocessing.dcm_converter import convert_dicom_to_nifti
from preprocessing.preprocessor import preprocess_nifti
from segmentation.inference import run_segmentation
from visualization.overlay import create_overlay_images

router = APIRouter()

@router.post("/segment-mri/")
async def segment_mri(file: UploadFile = File(...)):
    try:
        # Check if upload directory exists
        if not os.path.exists(settings.UPLOAD_DIR):
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            
        # Check if file is provided
        if not file or not file.filename:
            return JSONResponse(
                status_code=400, 
                content={"error": "No file uploaded or filename is empty"}
            )
            
        # Save uploaded file
        file_ext = os.path.splitext(file.filename)[1]
        upload_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        
        with open(upload_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Convert to NIfTI if necessary
        if file_ext.lower() in [".nii", ".nii.gz"]:
            nifti_path = upload_path
        elif file_ext.lower() == ".zip":
            dicom_folder = upload_path.replace(".zip", "")
            os.makedirs(dicom_folder, exist_ok=True)
            shutil.unpack_archive(upload_path, dicom_folder)
            nifti_path = convert_dicom_to_nifti(dicom_folder, upload_path.replace(".zip", ".nii"))
        else:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported file format: {file_ext}. Please upload .nii, .nii.gz, or .zip files"}
            )

        # Preprocess the NIfTI file
        preprocessed_path = preprocess_nifti(nifti_path)

        # Create inference input/output directories
        inference_input = os.path.join(settings.PROCESSED_DIR, "inference_input")
        inference_output = os.path.join(settings.PROCESSED_DIR, "inference_output")
        os.makedirs(inference_input, exist_ok=True)
        os.makedirs(inference_output, exist_ok=True)

        # Copy preprocessed file to input folder
        shutil.copy(preprocessed_path, os.path.join(inference_input, "preprocessed.nii.gz"))

        # Run inference
        model_path = os.path.join(settings.MODEL_DIR, "nnUNet", "3d_fullres", "Task220_MAMAMIA")
        prediction_path = run_segmentation(inference_input, inference_output, model_path)

        # Generate overlay images
        overlay_output_dir = os.path.join(settings.OUTPUT_DIR, "overlay_slices")
        os.makedirs(overlay_output_dir, exist_ok=True)
        create_overlay_images(preprocessed_path, prediction_path, overlay_output_dir)

        # Get list of overlay image filenames
        overlay_images = sorted(os.listdir(overlay_output_dir))

        # Return the prediction result
        return JSONResponse({
            "message": "Segmentation complete",
            "predicted_file": os.path.basename(prediction_path),
            "overlay_images": overlay_images
        })

    except FileNotFoundError as e:
        return JSONResponse(
            status_code=500, 
            content={"error": f"File not found: {str(e)}"}
        )
    except PermissionError as e:
        return JSONResponse(
            status_code=500, 
            content={"error": f"Permission error: {str(e)}. Check directory permissions."}
        )
    except Exception as e:
        # Log the full traceback for debugging
        error_traceback = traceback.format_exc()
        print(f"Error in segment_mri: {error_traceback}")
        
        return JSONResponse(
            status_code=500, 
            content={"error": f"An unexpected error occurred: {str(e)}"}
        )