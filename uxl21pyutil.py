"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is part of uxl21

    
    Author
    -----
    uxl21
"""

import json
import numpy
import pandas
import time

# from typing import Any, List, Tuple
from PyQt5.QtWidgets import *
from pandas.core.frame import DataFrame
from pandas.core.series import Series



class ListUtil:
    """
        Utility class for list(array).

        
        Author
        -----
        uxl21
    """ 

    @staticmethod
    def filterList(list:list, prop:str, filterValue:any) -> list:
        """
            Filters list items with their property name and value.

            Parameters
            ----------
            list: List
                Original data list
            prop: str
                property name of the item to filter
            filterValue: Any
                property value of the item to filter

            Returns
            -------
            List
                Contains filtered items

            Examples
            -----

            Author
            -----
            uxl21
        """
        numpy.array
        return [item for item in list if item[prop] != filterValue]


    @staticmethod
    def getMax(list:list, prop:any) -> any:
        """
            Returns the greatest value among array's item with its property name.
        """

        values = [item[prop] for item in list]

        #for item in list:
        #    values.append(item[prop])

        if len(values) > 0:
            return max(values)
        else:
            return None



class DataUtil:
    """
        Utility class for general data process

        
        Author
        -----
        uxl21
    """

    @staticmethod
    def isEmpty(value:any, trim:bool=False) -> bool:
        """
            Returns true if the value is null or empty string, zero-length array,
            false otherwise.

            
            Author
            -----
            uxl21
        """

        # check None
        if value == None:
            return True

        # check string
        if type(value) is str:
            strValue = value.strip() if trim else value
            
            if strValue == "":            
                return True

        # check list
        if type(value) is list and len(value) == 0:
            return True

        return False

    
    @staticmethod
    def isNotEmpty(value:any) -> bool:
        """
            Returns true if the value is not null and has value,
            false otherwise.

            
            Author
            -----
            uxl21
        """

        return not DataUtil.isEmpty(value)


    @staticmethod
    def isAnyEmpty(*args) -> bool:
        """
            Returns true if the one of the arguments is empty(DataUtil.isEmpty(value) is true),
            false otherwise.

            
            Author
            -----
            uxl21
        """

        for argValue in args:
            if DataUtil.isEmpty(argValue):
                return True
        
        return False


    @staticmethod
    def nvl(value:any, defaultValue:any) -> any:
        """
            Returns the default value if the value is empty(DataUtil.isEmpty(value) is true),
            original value otherwise.

            
            Author
            -----
            uxl21
        """

        if DataUtil.isEmpty(value):
            return defaultValue
        else:
            return value


    @staticmethod
    def ifelse(condition:bool, trueValue:any, falseValue:any) -> any:
        """
            Returns 'trueValue' if the given condition is True, 'falseValue' otherwise.

            
            Author
            -----
            uxl21
        """

        return trueValue if condition else falseValue


    @staticmethod
    def decode(value, *args) -> any:
        """
            'decode()' function just like Oracle DECODE()


            foo = "foo"

            value = DataUtil.decode(foo, "foo", "F", "X")
            print(value)    # => "F"

            value = DataUtil.decode(foo, "Xoo", "X", "foo", "F", "Zoo", "Z")
            print(value)    # => "F"

            
            Author
            -----
            uxl21
        """

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


    @staticmethod
    def toBoolean(value:any, default:bool=False) -> bool:
        """
            Returns boolean value from the given value.
            If value is empty, returns 'default'.

            
            Author
            -----
            uxl21
        """

        if DataUtil.isEmpty(value):
            return default

        else:
            if type(value) is str:
                return value.upper() == "Y" or value == "1"
            else:
                return bool(value)





class DictUtil:
    """
        Utility class for dictionary data

        
        Author
        -----
        uxl21
    """

    @staticmethod
    def isEmpty(data:dict, key:str) -> bool:
        """
            Returns true if the value of the dictionary for the specified key is a null or empty string, zero-length array,
            false otherwise.

            
            Author
            -----
            uxl21
        """
        
        return DataUtil.isEmpty(data.get(key))


    @staticmethod
    def isNotEmpty(data:dict, key:str) -> bool:
        """
            Returns true if the value of the dictionary for the specified key is not null and has value,
            false otherwise.

            
            Author
            -----
            uxl21
        """

        return not DictUtil.isEmpty(data, key)


    @staticmethod
    def hasKey(data:dict, keyToFind:str) -> bool:
        """
            Returns true if the dictionary has specified key,
            false otherwise.

            
            Author
            -----
            uxl21
        """

        hasThisKey = False
        keys = data.keys()

        for key in keys:
            if key == keyToFind:
                hasThisKey = True
                break

        return hasThisKey


    @staticmethod
    def getBoolean(data:dict, key:str, default:bool=False) -> bool:
        """
            Returns the value of the dictionary for the specified key as boolean type.

            
            Author
            -----
            uxl21
        """

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
        """
            Returns the value of the dictionary for the specified key as string type.

            
            Author
            -----
            uxl21
        """

        if DataUtil.isEmpty(data, key):
            return default
        else:
            return str(data.get(key))





class QWidgetUtil:
    """
        Utility class for QWidget

        
        Author
        -----
        uxl21
    """

    @staticmethod
    def createComboBox(items:list, parent:QWidget=None, initValue:any=None, currentTextChangedHandler=None) -> QComboBox:
        """
            Creates new instance of the QComboBox.


            Example
            -------
            combobox = QWidgetUtil.createComboBox(
                ["post", "get", "put"], initValue=s"post", currentTextChangedHandler=self.currentTextChangedHandler
            )

            
            Author
            -----
            uxl21
        """

        # create QComboBox instance
        comboBox = DataUtil.decode(parent, None, QComboBox(), QComboBox(parent))

        # add items
        for item in items:
            comboBox.addItem(item)

        # set initial value
        if DataUtil.isNotEmpty(initValue):
           comboBox.setCurrentText(initValue)

        # set handler for currentTextChanged event
        if DataUtil.isNotEmpty(currentTextChangedHandler):
            comboBox.currentTextChanged.connect(currentTextChangedHandler)

        return comboBox


    #
    # create QProgressDialog
    #
    @staticmethod
    def createProgressDialog(minimum:int=0, maximum:int=100, title:str="", label:str="", isModal:bool=True) -> QProgressDialog:
        """
            Creates new instance of QProgressDialog.
            
            Example
            -------
            progressDialog = QWidgetUtil.createProgressDialog(title="PLZ wait", label="In progress...", maximum=80)
            progressDialog.show()

            
            Author
            -----
            uxl21
        """
        progressDialog = QProgressDialog(label, None, minimum, maximum)
        progressDialog.setModal(isModal)
        progressDialog.setValue(0)
        progressDialog.setWindowTitle(title)
        progressDialog.setCancelButton(None)
        progressDialog.setAutoClose(False)

        return progressDialog





class DatetimeUtil:
    """
        Utility class for datetime process

        
        Author
        -----
        uxl21
    """

    class StopWatch:
        """
            The StopWatch class including lap time function.

            
            Author
            -----
            uxl21
        """

        def __init__(self, label:str="DEFAULT") -> None:
            self.__label = label
            self.__startTimeMs = 0
            self.__stopTimeMs = 0
            self.__lapTimes = []


        def start(self) -> None:
            """
                Starts to run timer.

                
            Author
            -----
            uxl21
            """

            self.__startTimeMs = int(time.time() * 1000)


        def lap(self) -> None:
            """
                Marks the lap time.

                
            Author
            -----
            uxl21
            """

            self.__lapTimes.append(int(time.time() * 1000))


        def stop(self) -> None:
            """
                Stops the timer/

                
            Author
            -----
            uxl21
            """

            self.__stopTimeMs = int(time.time() * 1000)


        def elapsed(self) -> int:
            """
                Returns the total elapsed time as milliseconds.

                
            Author
            -----
            uxl21
            """

            return self.__stopTimeMs - self.__startTimeMs


        def lapCount(self) -> int:
            """
                Returns the count of the marked lap time.

                
            Author
            -----
            uxl21
            """

            return len(self.__lapTimes)


        def lapTime(self, index:int) -> int:
            """
                Returns the lap time for the specified order(index).

                
            Author
            -----
            uxl21
            """

            if index >= len(self.__lapTimes):
                return -1

            return self.__lapTimes[index] - self.__startTimeMs


        def getLabel(self) -> str:
            """
                Returns the label.

                
            Author
            -----
            uxl21
            """

            return self.__label


        def reset(self) -> None:
            """
                Resets all lap times and elapsed time to zero.

                
            Author
            -----
            uxl21
            """

            self.__startTimeMs = 0
            self.__stopTimeMs = 0
            self.__lapTimes.clear()





class PandasUtil:
    """
        Utility class to process pandas data

    
        Author
        -----
        uxl21
    """

    @staticmethod
    def tooDict(series:Series) -> dict:
        """
            Converts the row data as pandas Series to dictionary

            Parameters
            --------
            series: pandas Series data to convert

            Examples
            --------
            data = [
                ["a", 2, 7],
                ["b", 5, 8],
                ["c", 7, 8]
            ]
            df = pd.DataFrame(data=data, columns=["COL1", "COL2", "COL3"])

            for rowIndex in range(len(df)):
                print( PandasUtil.toDict(df.iloc[rowIndex]) )

            `{'COL1': 'a', 'COL2': 2, 'COL3': 7}`
            `{'COL1': 'b', 'COL2': 5, 'COL3': 8}`
            `{'COL1': 'c', 'COL2': 7, 'COL3': 8}`

            
            Author
            -----
            uxl21
        """

        dictData = {}

        for col in series.index:
            dictData[col] = series[col]

        return dictData


    def toDictArray(df:DataFrame) -> list:
        """
            Converts pandas DataFrame data to array containing dictionary

            Parameters
            --------
            series: pandas Series data to convert

            Examples
            --------
            data = [
                ["a", 2, 7],
                ["b", 5, 8],
                ["c", 7, 8]
            ]

            df = pd.DataFrame(data=data, columns=["COL1", "COL2", "COL3"])

            print( PandasUtil.toDictArray(df) )
            `[{'COL1': 'a', 'COL2': 2, 'COL3': 7}, {'COL1': 'b', 'COL2': 5, 'COL3': 8}, {'COL1': 'c', 'COL2': 7, 'COL3': 8}]`

            
            Author
            -----
            uxl21
        """

        dictArray = []

        for rowIndex in range(len(df)):
            dictArray.append(PandasUtil.toDict(df.iloc[rowIndex]))

        return dictArray




if __name__ == "__main__":
    stopWatch = DatetimeUtil.StopWatch()
    stopWatch.start()

    data = numpy.loadtxt("./ratings.dat", delimiter="::", dtype=numpy.int64)
    stopWatch.lap()

    data = numpy.loadtxt("./ratings.dat", delimiter="::", dtype=numpy.int64)
    stopWatch.lap()

    data = numpy.loadtxt("./ratings.dat", delimiter="::", dtype=numpy.int64)
    stopWatch.lap()

    for i in range(stopWatch.lapCount()):
        print("[" + str(i) + "]: " + str(stopWatch.lapTime(i)))
