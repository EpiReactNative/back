import io
import imghdr


def get_file_extension(filename, decoded_file):
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow is not installed.")
    extension = imghdr.what(filename, decoded_file)

    if extension is None:
        try:
            image = Image.open(io.BytesIO(decoded_file))
        except (OSError, IOError):
            raise

        extension = image.format.lower()

    extension = "jpg" if extension == "jpeg" else extension
    return extension
