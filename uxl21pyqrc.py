"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is a part of uxl21py

    
    Author
    -----
    uxl21
"""
from base64 import encode
from sys import version

from qrcode import constants
from uxl21pyutil import DataUtil, DictUtil
import qrcode
import pyqrcode
from qrcode.main import QRCode


class QRCodeImageConstants:

    """
        Default version of the QR code.
    """
    DEFAULT_VERSION = 1

    """
        Default box size of the QR code.
    """
    DEFAULT_BOX_SIZE = 10

    """
        Default border of the QR code.
    """
    DEFAULT_BORDER = 4

    """
        Default fill colour of the QR code.
    """
    DEFAULT_FILL_COLOUR = "#000000"    # "#2e4e96"

    """
        Default background colour of the QR code.
    """
    DEFAULT_BACKGROUND_COLOUR = "#ffffff"

    ERROR_CORRECT_H = constants.ERROR_CORRECT_H
    ERROR_CORRECT_L = constants.ERROR_CORRECT_L
    ERROR_CORRECT_M = constants.ERROR_CORRECT_M
    ERROR_CORRECT_Q = constants.ERROR_CORRECT_Q


    QRCODE_IMAGE_TYPE_PNG = "png"
    QRCODE_IMAGE_TYPE_SVG = "svg"
    QRCODE_IMAGE_TYPE_EPS = "eps"
    QRCODE_IMAGE_TYPE_XBM = "xbm"



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
                - version: QR code version between 1 and 40. Default is QRCodeImageConstants.DEFAULT_VERSION(1)
                - errorCorrection: Error correction
                    - QRCodeImageConstants.ERROR_CORRECT_H
                    - QRCodeImageConstants.ERROR_CORRECT_L
                    - QRCodeImageConstants.ERROR_CORRECT_M
                    - QRCodeImageConstants.ERROR_CORRECT_Q
                - boxSize: Box size. Default is QRCodeImageConstants.DEFAULT_BOX_SIZE(10)
                - border: Border size. Default is QRCodeImageConstants.DEFAULT_BORDER(4)

            Author
            -------
            uxl21
        """

        self.version = DictUtil.getInteger(kargs, "version", QRCodeImageConstants.DEFAULT_VERSION)
        self.errorCorrection = DictUtil.getInteger(kargs, "errorCorrection", QRCodeImageConstants.ERROR_CORRECT_M)
        self.boxSize = DictUtil.getInteger(kargs, "boxSize", QRCodeImageConstants.DEFAULT_BOX_SIZE)
        self.border = DictUtil.getInteger(kargs, "border", QRCodeImageConstants.DEFAULT_BORDER)

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
                the dictionary data containing 'fillColour' and 'backgroundColour'

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

    @staticmethod
    def generate(qrCodeData:any, path:str, type:str="png", **kargs) -> None:
        encode = DictUtil.getString(kargs, "encoding", "utf-8")
        scale = DictUtil.getInteger(kargs, "scale", 1)
        moduleColour = DictUtil.getInteger(kargs, "moduleColour", QRCodeImageConstants.DEFAULT_FILL_COLOUR)
        backgroundColour = DictUtil.getInteger(kargs, "backgroundColour", QRCodeImageConstants.DEFAULT_BACKGROUND_COLOUR)

        qr = pyqrcode.create(qrCodeData, encoding=encode)
        loweredType = type.lower()

        if loweredType == QRCodeImageConstants.QRCODE_IMAGE_TYPE_PNG:
            callMethod = qr.png
        elif loweredType == QRCodeImageConstants.QRCODE_IMAGE_TYPE_SVG:
            callMethod = qr.svg
        elif loweredType == QRCodeImageConstants.QRCODE_IMAGE_TYPE_EPS:
            callMethod = qr.eps
        elif loweredType == QRCodeImageConstants.QRCODE_IMAGE_TYPE_XBM:
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

    generator = QRCodeImageGenerator(version=1, boxSize=3, border=2)
    generator.addData(qrCodeData1)
    # generator.clearData()
    # generator.addData(qrCodeData2)
    generator.generate("D:\\qrcode1.png")

    SimplePyQRCodeGenerator.generate(qrCodeData2, "D:\\qrcode2.png", encoding="utf-8")


