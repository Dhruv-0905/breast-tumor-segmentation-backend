import os
import SimpleITK as sitk

def convert_dicom_to_nifti(dicom_dir: str, output_path: str):
    reader = sitk.ImageSeriesReader()
    dicom_series = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_series)
    
    image = reader.Execute()
    sitk.WriteImage(image, output_path)
    return output_path
