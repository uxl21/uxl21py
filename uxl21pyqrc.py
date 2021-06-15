"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is a part of uxl21py

    
    Author
    -----
    uxl21
"""
from platform import version
from textwrap import fill
from _pytest._io.wcwidth import wcwidth
import qrcode
from qrcode.main import QRCode


class QRCodeImageGenerator:
    """
        This class generates QR code image.

        Author
        -----
        uxl21
    """
    
    def __init__(self) -> None:
        print("QR Code Image Genrator")



if __name__ == "__main__":
    qrCodeData = """
        {
            title: "Naver Blog",
            url: "https://blog.naver.com/uxl21"
        }
    """

    qr = qrcode.QRCode(
        version=8
        # box_size=10,
        # border=4
    )
    qr.add_data(qrCodeData)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#333333", back_color="#ffffff")
    # img.width = 10
    # img.pixel_size = 100
    img.save("/Volumes/OPSLAGPLAATS/WERKTAFEL/qrcode8.png", "png")

    # img.pixel_size = (img.width + img.border * 2) * img.box_size
    # 490 = (41 + 4 * 2) * 10

    print()
    print(img.pixel_size, img.width, img.box_size, img.border)