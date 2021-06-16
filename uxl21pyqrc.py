"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is a part of uxl21py

    
    Author
    -----
    uxl21
"""
from base64 import encode
from sys import setcheckinterval, version

from qrcode import constants
from uxl21pyutil import DataUtil, DictUtil
import pyqrcode
from qrcode.main import QRCode


class QRCodeImageConstants:
    """
        This class defines constants for QR code image commonly.
        Some constants are for QRCodeImageGenerator class and the others are for SimplePyQRCodeGenerator.

        Author
        -------
        uxl21
    """


    """
        Default fill colour of the QR code.
    """
    DEFAULT_FILL_COLOUR = "#000000"    # "#2e4e96"

    """
        Default background colour of the QR code.
    """
    DEFAULT_BACKGROUND_COLOUR = "#ffffff"


    # for QRCodeImageGenerator class
    """
        Default version of the QR code.
    """
    QRCODE_DEFAULT_VERSION = 1

    """
        Default box size of the QR code.
    """
    QRCODE_DEFAULT_BOX_SIZE = 10

    """
        Default border of the QR code.
    """
    QRCODE_DEFAULT_BORDER = 4

    QRCODE_ERROR_CORRECT_H = constants.ERROR_CORRECT_H
    QRCODE_ERROR_CORRECT_Q = constants.ERROR_CORRECT_Q
    QRCODE_ERROR_CORRECT_M = constants.ERROR_CORRECT_M
    QRCODE_ERROR_CORRECT_L = constants.ERROR_CORRECT_L


    # for SimplePyQRCodeGenerator class
    """
        Default version of the QR code.
    """
    PYQRCODE_DEFAULT_VERSION = 10

    PYQRCODE_ERROR_CORRECT_H = "H"
    PYQRCODE_ERROR_CORRECT_Q = "Q"
    PYQRCODE_ERROR_CORRECT_M = "M"
    PYQRCODE_ERROR_CORRECT_L = "L"

    PYQRCODE_IMAGE_TYPE_PNG = "png"
    PYQRCODE_IMAGE_TYPE_SVG = "svg"
    PYQRCODE_IMAGE_TYPE_EPS = "eps"
    PYQRCODE_IMAGE_TYPE_XBM = "xbm"

    """
        Default scale value for the QR code image created by SimplePyQRCodeImageGenerator class.
    """
    PYQRCODE_DEFAULT_SCALE = 2




class QRCodeImageGenerator:
    """
        This class generates QR code image.

        Author
        -----
        uxl21
    """


    def __init__(self, **kargs) -> None:
        """
            Constructor

            Parameters
            -------
            kargs: dict
                - version: QR code version between 1 and 40. Default is QRCodeImageConstants.QRCODE_DEFAULT_VERSION(1)
                - errorCorrection: Error correction
                    - QRCodeImageConstants.QRCODE_ERROR_CORRECT_H
                    - QRCodeImageConstants.QRCODE_ERROR_CORRECT_Q
                    - QRCodeImageConstants.QRCODE_ERROR_CORRECT_M
                    - QRCodeImageConstants.QRCODE_ERROR_CORRECT_L
                - boxSize: Box size. Default is QRCodeImageConstants.DEFAULT_BOX_SIZE(10)
                - border: Border size. Default is QRCodeImageConstants.DEFAULT_BORDER(4)

            Author
            -------
            uxl21
        """
        
        self.version = DictUtil.getInteger(kargs, "version", QRCodeImageConstants.QRCODE_DEFAULT_VERSION)
        self.errorCorrection = DictUtil.getInteger(kargs, "errorCorrection", QRCodeImageConstants.QRCODE_ERROR_CORRECT_M)
        self.boxSize = DictUtil.getInteger(kargs, "boxSize", QRCodeImageConstants.QRCODE_DEFAULT_BOX_SIZE)
        self.border = DictUtil.getInteger(kargs, "border", QRCodeImageConstants.QRCODE_DEFAULT_BORDER)

        self.fillColour = QRCodeImageConstants.DEFAULT_FILL_COLOUR
        self.backgroundColour = QRCodeImageConstants.DEFAULT_BACKGROUND_COLOUR
        
        self.qr = QRCode(version=self.version, error_correction=self.errorCorrection, box_size=self.boxSize, border=self.border)


    def setColours(self, **kargs) -> None:
        """
            Sets the fill and background colours.
            The colour value should be a hex code or a string representing colours.

            Parameters
            -------
            kargs: dict
                the dictionary data containing 'fillColour' and 'backgroundColour' attributes.

            Author
            -------
            uxl21
        """

        if DictUtil.isNotEmpty(kargs, "fillColour"):
            self.fillColour = DictUtil.getString(kargs, "fillColour")
            
        if DictUtil.isNotEmpty(kargs, "backgroundColour"):
            self.backgroundColour = DictUtil.getString(kargs, "backgroundColour")


    def addData(self, data:any) -> None:
        """
            Adds QR code data.

            Parameters
            -------
            data: any
                data to add

            Author
            -------
            uxl21
        """

        if DataUtil.isNotEmpty(data):
            self.qr.add_data(data)


    def clearData(self) -> None:
        """
            Clears all data.

            Author
            -------
            uxl21
        """

        self.qr.clear()


    def generate(self, path:str, type="PNG") -> None:
        """
            Generates the QR code image file.
            
            Parameters
            -------
            path: str
                Absolute path including file name and extension.
            type: str
                Image file type. Default is 'PNG'.

            Author
            -------
            uxl21
        """

        self.qr.make()

        img = self.qr.make_image(fill_color=self.fillColour, back_color=self.backgroundColour)
        img.save(path, type)



class SimplePyQRCodeGenerator:
    """
        This class generates QR code image with string data simply.

        Author
        -------
        uxl21
    """

    @staticmethod
    def generate(qrCodeData, path:str, **kargs) -> None:
        """
            Generates QR code image with string data and some configurations.

            Parameters
            -------
            qrCodeData: str
                string data
            path: str
                Absolute path including file name and extension.
            type: str
                - QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_PNG (Default)
                - QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_SVG
                - QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_EPS
                - QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_XBM
            kargs: dict
                - version: QR code version between 1 and 40. Default is QRCodeImageConstants.PYQRCODE_DEFAULT_VERSION(10)
                - encoding: encoding of the string data. Default is utf-8.
                - scale: QR code image's scale. Default is QRCodeImageConstants.PYQRCODE_DEFAULT_SCALE(2).
                - errorCorrection: Error correction
                    - QRCodeImageConstants.PYQRCODE_ERROR_CORRECT_H
                    - QRCodeImageConstants.PYQRCODE_ERROR_CORRECT_Q
                    - QRCodeImageConstants.PYQRCODE_ERROR_CORRECT_M (Default)
                    - QRCodeImageConstants.PYQRCODE_ERROR_CORRECT_L

            Author
            -------
            uxl21
        """

        print(kargs)
        type = DictUtil.getString(kargs, "type", QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_PNG)
        version = DictUtil.getInteger(kargs, "version", QRCodeImageConstants.PYQRCODE_DEFAULT_VERSION)
        errorCorrection = DictUtil.getString(kargs, "errorCorrection", QRCodeImageConstants.PYQRCODE_ERROR_CORRECT_M)
        encode = DictUtil.getString(kargs, "encoding", "utf-8")
        scale = DictUtil.getInteger(kargs, "scale", QRCodeImageConstants.PYQRCODE_DEFAULT_SCALE)
        moduleColour = DictUtil.getInteger(kargs, "fillColour", QRCodeImageConstants.DEFAULT_FILL_COLOUR)
        backgroundColour = DictUtil.getInteger(kargs, "backgroundColour", QRCodeImageConstants.DEFAULT_BACKGROUND_COLOUR)

        qr = pyqrcode.create(qrCodeData, error="H", version=version, encoding=encode)
        loweredType = type.lower()

        if loweredType == QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_PNG:
            callMethod = qr.png
        elif loweredType == QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_SVG:
            callMethod = qr.svg
        elif loweredType == QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_EPS:
            callMethod = qr.eps
        elif loweredType == QRCodeImageConstants.PYQRCODE_IMAGE_TYPE_XBM:
            callMethod = qr.xbm
        else:
            callMethod = qr.png

        callMethod(path, scale=scale, module_color=moduleColour, background=backgroundColour)
        
    



if __name__ == "__main__":
    qrCodeData1 = """
        {
            title: "네이버 Blog",
            url: "https://blog.naver.com/uxl21"
        }
    """
    qrCodeData2 = {
        "title": "Naver Sub Blog",
        "url": "https://blog.naver.com/uxl21x"
    }

    generator = QRCodeImageGenerator(version=1, boxSize=4, border=2)
    generator.setColours(fillColour="#2e4e96")
    generator.addData(qrCodeData1)
    # generator.clearData()
    generator.addData(qrCodeData2)
    generator.generate("./qrcode.png")

    SimplePyQRCodeGenerator.generate(qrCodeData1, "./pyqrcode.png", scale=3)