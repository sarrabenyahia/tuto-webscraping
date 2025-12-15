"""
QR Code Generator
Generates a QR code image from a URL or any text.

Installation:
    pip install qrcode pillow
"""

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def generate_qr_code(data: str, filename: str = "qrcode.png", box_size: int = 10, border: int = 4):
    """
    Generate a QR code from the given data and save it as an image.
    
    Args:
        data: The URL or text to encode in the QR code
        filename: Output filename (default: qrcode.png)
        box_size: Size of each box in pixels (default: 10)
        border: Border size in boxes (default: 4)
    
    Returns:
        The filename of the saved QR code image
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create the QR code image with rounded corners for a modern look
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer()
    )
    
    img.save(filename)
    print(f"✓ QR code saved as '{filename}'")
    return filename


if __name__ == "__main__":
    # Example usage
    url = "https://docs.google.com/forms/d/e/1FAIpQLSfTRzgjomMKIsf4NJ7N-FHa94DfpNMwSRyRfKyEyyUPUYWLdg/viewform?usp=dialog"
    generate_qr_code(url, "qrcode.png")