"""Image resolution & standardization helper for rendering uniform product images in Streamlit."""

import base64
import io
import os
from PIL import Image

_IMAGE_CACHE = {}


def get_image_src(path_or_url: str, target_size=(300, 300)) -> str:
    """Convert local file path to standardized 300x300 base64 Data URI for uniform product image sizes."""
    if not path_or_url:
        return ""
    if path_or_url.startswith("http://") or path_or_url.startswith("https://") or path_or_url.startswith("data:"):
        return path_or_url

    if path_or_url in _IMAGE_CACHE:
        return _IMAGE_CACHE[path_or_url]

    if os.path.exists(path_or_url):
        try:
            with Image.open(path_or_url) as img:
                img = img.convert("RGBA")
                # Create uniform canvas with subtle light background (#F8FAF8)
                background = Image.new("RGBA", target_size, (248, 250, 248, 255))
                
                # Scale image while maintaining original aspect ratio
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                
                # Center image on canvas
                x = (target_size[0] - img.width) // 2
                y = (target_size[1] - img.height) // 2
                background.paste(img, (x, y), img)
                
                # Save as clean JPEG
                final_img = background.convert("RGB")
                buf = io.BytesIO()
                final_img.save(buf, format="JPEG", quality=90)
                encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
                
                data_uri = f"data:image/jpeg;base64,{encoded}"
                _IMAGE_CACHE[path_or_url] = data_uri
                return data_uri
        except Exception:
            # Fallback to direct file reading if PIL fails
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
