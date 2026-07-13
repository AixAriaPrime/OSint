from typing import Dict, Any

class ImageMetadata:
    """Extract EXIF, XMP, IPTC metadata from images"""
    
    @staticmethod
    async def extract(image_path_or_url: str) -> Dict[str, Any]:
        
        return 
            "input": image_path_or_url,
            "exif_data": {
                "datetime": "DateTimeOriginal, DateTimeDigitized",
                "gps": "GPSLatitude, GPSLongitude, GPSAltitude",
                "device": "Make, Model, Software",
                "camera": "LensModel, FocalLength, FNumber, ExposureTime, ISO",
                "image": "ImageWidth, ImageLength, ColorSpace",
                "other": "Orientation, Flash, WhiteBalance, MeteringMode"
            ,
            "gps_data": 
                "can_reveal": "Exact capture location",
                "note": "Many modern devices strip GPS by default",
                "tools": ["exiftool", "exifread", "Jeffrey's EXIF Viewer"]
            ,
            "device_info": 
                "can_find": "Camera model, phone model, software version",
                "privacy_risk": "High"
            ,
            "tools": [
                "name": "ExifTool", "url": "https://exiftool.org/",
                "name": "Jeffrey's EXIF Viewer", "url": "https://exifviewer.org/",
                "name": "FotoForensics", "url": "https://fotoforensics.com/"
            ]
  }
