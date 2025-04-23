from flask import request, jsonify
import os

class FileService:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

    def save_file(self, file):
        if file and self.allowed_file(file.filename):
            filename = self.secure_filename(file.filename)
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            return filename
        return None

    def allowed_file(self, filename):
        allowed_extensions = {'dcm', 'nii', 'nii.gz'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def secure_filename(self, filename):
        return filename.replace(" ", "_").replace("..", "")  # Simple sanitization

    def get_file_path(self, filename):
        return os.path.join(self.upload_folder, filename) if filename else None

    def delete_file(self, filename):
        file_path = self.get_file_path(filename)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False