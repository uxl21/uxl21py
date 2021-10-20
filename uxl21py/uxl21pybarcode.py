##################################################
#   Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
#   This file is a part of uxl21py
# 
#   Author: uxl21
##################################################

import os
from PIL.Image import Image
import barcode
from barcode.writer import ImageWriter
from pyzbar import pyzbar
import cv2


class BarcodeFormat:
    """
        This class define the barcode formats.

        Author
        -------
        uxl21
    """

    EAN = "ean"
    EAN8 = "ean8"
    EAN13 = "ean13"
    EAN14 = "ean14"
    GTIN = "gtin"
    JAN = "jan"
    UPC = "upc"
    UPCA = "upca"
    ISBN = "isbn"
    ISBN10 = "isbn10"
    ISBN13 = "isbn13"
    ISSN = "issn"
    CODE39 = "code39"
    CODE128 = "code128"
    PZN = "pzn"
    ITF = "itf"
    GS1 = "gs1"
    GS1_128 = "gs1_128"



class BarcodeImageGenerator:
    """
        This class generates barcode image file.

        Author
        -------
        uxl21
    """

    def __init__(self, barcodeFormat:str) -> None:
        """
            Constructor

            Parameters
            -------
            barcodeFormat: str
                Barcode format defined in BarcodeFormat class.

            Author
            -------
            uxl21
        """

        self.format = barcodeFormat
        self.barcodeWriter = barcode.get_barcode_class(barcodeFormat)
        self.imageWriter = ImageWriter()


    def generate(self, barcodeData:str, path:str, title:str=None) -> str:
        """
            Generates a barcode image file with data.

            Parameters
            -------
            barcodeData: str
                Barcode data
            path: str
                File's path to save
            title: str
                Barcode image title and it will be file name

            Returns
            -------
            The absolute name with path of the saved image file

            Author
            -------
            uxl21
        """

        barcodeObj = self.barcodeWriter(barcodeData, writer=self.imageWriter)
        fileName = title if (title != None) else "barcode_" + self.format
        barcodeImageFile = barcodeObj.save(path + os.sep + fileName)

        return barcodeImageFile


    def write(self, barcodeData:str, filePath:str) -> None:
        """
            Writes a barcode image file with data.

            Parameters
            -------
            barcodeData: str
                Barcode data
            filePath: str
                The absolute path of the barcode image file to save including name and extension

            Author
            -------
            uxl21
        """

        barcodeObj = self.barcodeWriter(barcodeData, writer=self.imageWriter)
        barcodeObj.write(filePath)





class SimpleBarcodeImageReader:
    """
        This class reads barcode data from image file simply.

        Author
        -------
        uxl21
    """

    @staticmethod
    def read(input:str, encoding:str="utf-8") -> dict:
        """
            Reads barcode data from image file.

            Parameters
            -------
            input: str
                The absolute path of the image file to read
            encoding: str
                Encoding for barcode data. Default is 'utf-8'

            Author
            -------
            uxl21
        """

        image = cv2.imread(input)
        barcode = pyzbar.decode(image)
        data = {
            "type": None,
            "data": None
        }

        if barcode != None and len(barcode) > 0:
            decodedData = barcode[0]
            data["type"] = decodedData.type
            data["data"] = decodedData.data.decode(encoding)

        return data
