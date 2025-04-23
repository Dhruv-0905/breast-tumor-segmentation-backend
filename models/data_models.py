from pydantic import BaseModel
from typing import List, Optional

class ImageUploadRequest(BaseModel):
    file: str  # Path to the uploaded DCE-MRI image file

class SegmentationResponse(BaseModel):
    segmentation_mask: str  # Path to the generated segmentation mask
    original_image: str  # Path to the original image
    confidence_scores: Optional[List[float]] = None  # Optional confidence scores for the segmentation

class ErrorResponse(BaseModel):
    detail: str  # Error message detailing what went wrong

class HealthCheckResponse(BaseModel):
    status: str  # Health status of the application (e.g., "healthy")