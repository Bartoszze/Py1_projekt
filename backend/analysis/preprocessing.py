import cv2
import os

def get_image_metadata(path: str):
    img = cv2.imread(path)
    if img is None:
        return None
    h, w, c = img.shape
    size = os.path.getsize(path)
    return {"width": w, "height": h, "channels": c, "size_bytes": size}
