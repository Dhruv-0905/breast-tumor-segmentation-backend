def log_message(message):
    print(f"[LOG] {message}")

def handle_error(error):
    log_message(f"[ERROR] {error}")
    # Additional error handling logic can be added here

def validate_file_extension(filename, allowed_extensions):
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        handle_error(f"Invalid file extension for {filename}. Allowed extensions are: {allowed_extensions}")
        return False
    return True

def save_uploaded_file(uploaded_file, destination):
    try:
        with open(destination, 'wb') as f:
            f.write(uploaded_file.read())
        log_message(f"File saved to {destination}")
    except Exception as e:
        handle_error(f"Failed to save file: {e}")