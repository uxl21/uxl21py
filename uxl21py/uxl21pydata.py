"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is a part of uxl21py

    uxl21pydata.py

    Author
    -----
    uxl21
"""


import json
from typing import Any


class Stack:
    """
        This class represents the stack data structure.

        Author:
            uxl21
    """

    def __init__(self) -> None:
        """
            Constructor

            Author:
                uxl21
        """

        self.__list = []


    def __str__(self) -> str:
        return str(self.__list)


    def push(self, item) -> None:
        """
            Pushes a new item into the stack.

            Parameters:
                item : any
                    A new item to push

            Author:
                uxl21
        """

        self.__list.append(item)


    def pop(self) -> any:
        """
            Returns the lastest item from the stack.

            Returns:
                any : The lastest item from the stsack

            Author:
                uxl21
        """

        if self.isEmpty():
            raise IndexError("Stack underflow")
        else:
            return self.__list.pop(-1)


    def peek(self) -> any:
        """
            Returns the last item from the stack.

            Returns:
                any : The last item from the stsack

            Author:
                uxl21
        """

        if self.isEmpty():
            raise IndexError("Stack underflow")
        else:
            return self.__list[-1]


    def clear(self) -> None:
        """
            Remove all items from the stack.

            Author:
                uxl21
        """

        self.__list.clear()


    def size(self) -> int:
        """
            Returns the size of the stack

            Returns:
                bool : The size of the stack

            Author:
                uxl21
        """

        return len(self.__list)


    def isEmpty(self) -> bool:
        """
            Returns whether the stack is empty or not.

            Returns:
                bool : Whether the stack is empty or not

            Author:
                uxl21
        """

        return len(self.__list) == 0


    def contains(self, item) -> bool:
        """
            Returns whether the stack contains a specified item or not.

            Parameters:
                item : any
                    Item to check

            Returns:
                bool : Whether the stack contains a specified item or not

            Author:
                uxl21
        """

        return item in self.__list





class JSONConfigData():
    """
        The configuration utility class that loads and uses JSON data.

        Author
        -------
        uxl21
    """


    #
    # constructor
    #
    def __init__(self, jsonPath:str) -> None:
        configFile = open(jsonPath, "r")

        # read
        jsonStr = configFile.read()
        
        # load
        self.__configData = json.loads(jsonStr)

        configFile.close()


    def getConfig(self, configName:str) -> Any:
        """
            Returns config value of the specified name.

            Parameters:
                list : list
                    Original data list
                
            Returns:
                Any
                    Config value

            Author:
                uxl21
        """
        
        return self.__configData[configName]
