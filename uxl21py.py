"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is part of uxl21

    @author uxl21
"""

import json

from typing import Any, List, Tuple
from PyQt5.QtWidgets import *


"""
    Utility class for List

    @author uxl21
"""
class ListUtil:

    """
        Filters list items with its property name and value.

        @author uxl21
    """
    @staticmethod
    def filterList(list:List, prop:str, filterValue:Any) -> List:
        return [item for item in list if item[prop] != filterValue]


    """
        Returns the greatest value among array's item with its property name.
    """
    @staticmethod
    def getMax(list:List, prop:Any) -> Any:
        values = [item[prop] for item in list]

        #for item in list:
        #    values.append(item[prop])

        if len(values) > 0:
            return max(values)
        else:
            return None



"""
    Utility class for general data process
"""
class DataUtil:

    """
        Returns true if the value is null or empty string, zero-length array,
        false otherwise.

        @author uxl21
    """
    @staticmethod
    def isEmpty(value:Any, trim:bool=False) -> bool:
        # None check
        if value == None:
            return True

        # string check
        if type(value) is str:
            strValue = value.strip() if trim else value
            
            if strValue == "":            
                return True

        # list check
        if type(value) is list and len(value) == 0:
            return True

        return False

    
    """
        Returns true if the value is not null and has value,
        false otherwise.

        @author uxl21
    """
    @staticmethod
    def isNotEmpty(value:Any) -> bool:
        return not DataUtil.isEmpty(value)


    """
        Returns true if the one of the arguments is empty(DataUtil.isEmpty(value) is true),
        false otherwise.

        @author uxl21
    """
    @staticmethod
    def isAnyEmpty(*args) -> bool:
        for argValue in args:
            if DataUtil.isEmpty(argValue):
                return True
        
        return False


    """
        Returns the default value if the value is empty(DataUtil.isEmpty(value) is true),
        original value otherwise.

        @author uxl21
    """
    @staticmethod
    def nvl(value:Any, defaultValue:Any) -> Any:
        if DataUtil.isEmpty(value):
            return defaultValue
        else:
            return value


    """
        Returns 'trueValue' if the given condition is True, 'falseValue' otherwise.

        @author uxl21
    """
    @staticmethod
    def ifelse(condition:bool, trueValue:Any, falseValue:Any) -> Any:
        return trueValue if condition else falseValue


    """
        'decode()' function just like Oracle DECODE()


        foo = "foo"

        value = DataUtil.decode(foo, "foo", "F", "X")
        print(value)    # => "F"

        value = DataUtil.decode(foo, "Xoo", "X", "foo", "F", "Zoo", "Z")
        print(value)    # => "F"

        @author uxl21
    """
    @staticmethod
    def decode(value, *args) -> Any:
        length = len(args)

        if length < 2:
            return value

        i = index = 0
        count = length // 2
        decodedValue = None

        while i < count:
            if value == args[index]:
                decodedValue = args[index + 1]

            index += 2
            i += 1
        
        # in case of no matched value, 
        # if args length is even, returns the original value or else the last element of args
        if decodedValue == None:
            decodedValue = value if (length % 2 == 0) else args[length - 1]
        
        return decodedValue


    """
        Returns boolean value from the given value.
        If value is empty, returns 'default'.
    """
    @staticmethod
    def toBoolean(value:Any, default:bool=False) -> bool:
        if DataUtil.isEmpty(value):
            return default

        else:
            if type(value) is str:
                return value.upper() == "Y" or value == "1"
            else:
                return bool(value)





"""
    Utility class for dictionary data

    @author uxl21
"""
class DictUtil:

    @staticmethod
    def isEmpty(data:dict, key:str) -> bool:
        return DataUtil.isEmpty(data.get(key))


    @staticmethod
    def isNotEmpty(data:dict, key:str) -> bool:
        return not DictUtil.isEmpty(data, key)


    @staticmethod
    def hasKey(data:dict, keyToFind:str) -> bool:
        hasThisKey = False
        keys = data.keys()

        for key in keys:
            if key == keyToFind:
                hasThisKey = True
                break

        return hasThisKey


    @staticmethod
    def getBoolean(data:dict, key:str, default:bool=False) -> bool:
        if DataUtil.isEmpty(data, key):
            return default

        else:
            value = data.get(key)

            if type(value) is str:
                return value.upper() == "Y" or value == "1"
            else:
                return bool(value)


    @staticmethod
    def getString(data:dict, key:str, default:str="") -> str:
        if DataUtil.isEmpty(data, key):
            return default
        else:
            return str(data.get(key))





#
# Utility class for QWidget
#
class QWidgetUtil:

    #
    # create QComboBox
    #
    @staticmethod
    def createComboBox(items:List, parent:QWidget=None, initValue:Any=None, currentTextChangedHandler=None) -> QComboBox:
        comboBox = DataUtil.decode(parent, None, QComboBox(), QComboBox(parent))

        for item in items:
            comboBox.addItem(item)


        if DataUtil.isNotEmpty(initValue):
           comboBox.setCurrentText(initValue)

        if DataUtil.isNotEmpty(currentTextChangedHandler):
            comboBox.currentTextChanged.connect(currentTextChangedHandler)

        return comboBox


    #
    # create QProgressDialog
    #
    @staticmethod
    def createProgressDialog(minimum:int=0, maximum:int=100, title:str="", label:str="", isModal:bool=True) -> QProgressDialog:
        progressDialog = QProgressDialog(label, None, minimum, maximum)
        progressDialog.setModal(isModal)
        progressDialog.setValue(0)
        progressDialog.setWindowTitle(title)
        progressDialog.setCancelButton(None)
        progressDialog.setAutoClose(False)

        return progressDialog




if __name__ == "__main__":
    dataObj = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
        "key4": "value4",
        "key5": "value5",
        "key6": "value6",
        "key7": "value7",
        "key8": "value8"
    }

    print( json.dumps(dataObj) )
