import os


def remove_background(image_path, output_path=None):
    try:
        from rembg import remove
        from PIL import Image

        if output_path is None:
            root, _ = os.path.splitext(image_path)
            output_path = root + "_bg.png"

        image = Image.open(image_path).convert("RGBA")
        result = remove(image)
        result.save(output_path, "PNG")
        return output_path
    except Exception:
        return None


def is_available():
    try:
        import rembg  # noqa: F401
        return True
    except Exception:
        return False
