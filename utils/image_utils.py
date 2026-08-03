"""Image resolution helper for rendering local static image files in Streamlit HTML components."""

import base64
import os

_IMAGE_CACHE = {}

def get_image_src(path_or_url: str) -> str:
    """Convert local file path to base64 Data URI for seamless HTML <img> rendering, or return URL directly."""
    if not path_or_url:
        return ""
    if path_or_url.startswith("http://") or path_or_url.startswith("https://") or path_or_url.startswith("data:"):
        return path_or_url
    
    if path_or_url in _IMAGE_CACHE:
        return _IMAGE_CACHE[path_or_url]

    if os.path.exists(path_or_url):
        ext = os.path.splitext(path_or_url)[1].lower().replace(".", "")
        mime_type = "jpeg" if ext in ["jpg", "jpeg"] else ext
        try:
            with open(path_or_url, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            data_uri = f"data:image/{mime_type};base64,{encoded}"
            _IMAGE_CACHE[path_or_url] = data_uri
            return data_uri
        except Exception:
            return path_or_url

    return path_or_url
