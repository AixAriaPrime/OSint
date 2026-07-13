from typing import Any, Dict


class ImageMetadata:
    """EXIF metadata extraction helper."""

    @staticmethod
    async def extract(image_path_or_url: str) -> Dict[str, Any]:
        return {
            "input": image_path_or_url,
            "exif_data": {
                "datetime": ["DateTimeOriginal", "DateTimeDigitized"],
                "gps": ["GPSLatitude", "GPSLongitude", "GPSAltitude"],
                "device": ["Make", "Model", "Software"],
                "camera": ["LensModel", "FocalLength", "FNumber", "ExposureTime", "ISO"],
                "image": ["ImageWidth", "ImageLength", "ColorSpace"],
            },
            "gps_data": {
                "can_reveal": "Capture location if present.",
                "note": "Many services remove GPS metadata automatically.",
                "tools": ["exiftool", "exifread", "Jeffrey's EXIF Viewer"],
            },
            "device_info": {
                "can_find": "Camera or phone model and software metadata.",
                "privacy_risk": "High",
            },
            "tools": [
                {"name": "ExifTool", "url": "https://exiftool.org/"},
                {"name": "Jeffrey's EXIF Viewer", "url": "http://regex.info/exif.cgi"},
                {"name": "FotoForensics", "url": "https://fotoforensics.com/"},
            ],
        }
