"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is a part of uxl21py

    uxl21pybatis.py
    
    Author
    -----
    uxl21
"""
from abc import *
from sqlite3.dbapi2 import Error
from xml.dom import Node, minidom

import re
import cx_Oracle    # pip install cx_Oracle
import sqlite3
import pymysql      # pip install PyMySQL


#
# for SQL Mapper
#

class PySQLMapper(metaclass=ABCMeta):
    """
        An abstract class defining methods for SQL mapper.

        Author
        -------
        uxl21
    """

    @abstractmethod
    def __init__(self, xmlPath:str) -> None: ...

    @abstractmethod
    def getQuery(self, id:str, parameter:dict) -> str: ...

    @abstractmethod
    def getResultType(self, id:str) -> str: ...





class PyBatisException(Exception):
    """
        The exception class for PyBatis

        Author
        -------
        uxl21
    """





class PybatisSQLMapper(PySQLMapper):
    """
        Pybatis SQL mapper class.

        Author
        -------
        uxl21
    """
    
    def __init__(self, xmlPath:str) -> None:
        self.__QUERY_TYPES = [ "select", "insert", "update", "delete", "sql" ]

        self.__xmlPath = xmlPath
        self.__xmldoc = None
        self.__namespace = ""
        self.__mapper = {}
        
        self.__createMapper()


    def __createMapper(self) -> None:
        self.__xmldoc = minidom.parse(self.__xmlPath)
        self.__namespace = self.__xmldoc.getElementsByTagName("mapper")[0].getAttribute("namespace")

        if self.__namespace == None or len(str(self.__namespace).strip()) == 0:
            raise PyBatisException("Mapper XML has to be specified the namespace attribute")

        for tag in self.__QUERY_TYPES:
            elementlist = self.__xmldoc.getElementsByTagName(tag)

            for element in elementlist:
                queryId = element.getAttribute("id")

                # when <sql> is child of the other node, it has no attribute 'id'
                if len(str(queryId)) > 0:
                    queryId = self.__namespace + "." + element.getAttribute("id")

                    if queryId in self.__mapper:
                        raise PyBatisException("SQL '{0}' is duplicated in mapper '{1}'".format(queryId, self.__xmlPath))
                    else:
                        self.__mapper[queryId] = element


    def __setAttrToAll(self, node:Node, attr, value, nodeFilter=None) -> None:
        if nodeFilter != None and node.nodeName != nodeFilter:
            return

        if node.hasChildNodes():
            for child in node.childNodes:
                self.__setAttrToAll(child, attr, value, nodeFilter)
        else:
            if node.hasAttribute(attr):
                node.setAttribute(attr, value)


    def __checkTest(self, test:str, parameter:dict) -> bool:
        replaced = re.sub("[n|N][u|U][l|L][l|L]", "None", test)

        for paramName in parameter:
            paramValue = "None" if parameter.get(paramName) == None else str(parameter[paramName])
            paramValue = re.sub("[n|N][u|U][l|L][l|L]", "None", paramValue)

            if paramValue == "None":
                replaced = replaced.replace(paramName, paramValue)
            else:
                replaced = replaced.replace(paramName, "'" + paramValue + "'")

        return eval(replaced)


    def __getQueryContent(self, node:Node, parameter:dict) -> None:
        sql = ""

        if node.hasChildNodes():
            if node.nodeName == "if":
                ifTest = self.__checkTest(node.attributes["test"].value, parameter)
                node.setAttribute("ifTest", ifTest)

                if ifTest:
                    for child in node.childNodes:
                        sql += self.__getQueryContent(child, parameter)                        
                else:
                    self.__setAttrToAll(node, "ifTest", False, "if")

            else:
                for child in node.childNodes:
                    sql += self.__getQueryContent(child, parameter)
            
        else:
            if node.parentNode.nodeName == "if":
                if node.parentNode.getAttribute("ifTest"):
                    if node.nodeName == "sql":
                        sql = self.__getQueryContent(self.__mapper[self.__namespace + "." + node.attributes["refid"].value], parameter)
                    else:
                        sql = str(node.nodeValue)                    
                else:
                    sql = ""
            else:
                # <sql refid="..."/>
                if node.nodeName == "sql" and node.hasAttribute("refid"):
                    sql += self.__getQueryContent(self.__mapper[self.__namespace + "." + node.attributes["refid"].value], parameter)
                else:
                    sql = "" if node.nodeValue == None else str(node.nodeValue)

        return sql


    def getQuery(self, id:str, parameter:dict=None) -> str:
        """
            Returns the query string for the specified id with parameter.

            Author
            -------
            uxl21
        """

        if id not in self.__mapper:
            raise PyBatisException("SQL '{0}' is not found in mapper '{1}'".format(id, self.__xmlPath))

        queryString = self.__getQueryContent(self.__mapper[id], parameter)
    
        if parameter != None:
            paramValue = None

            for paramName in parameter:
                if type(parameter[paramName]) is int or type(parameter[paramName]) is float:
                    queryString = queryString.replace("#{" + paramName + "}", str(parameter[paramName]))
                else:
                    queryString = queryString.replace("#{" + paramName + "}", "'" + str(parameter[paramName]).replace("'", "''") + "'")
                
                queryString = queryString.replace("${" + paramName + "}", str(parameter[paramName]))

        return queryString


    def getResultType(self, id:str) -> str:
        """
            Returns the resultType attribute's value for the specified query id.

            Author
            -------
            uxl21
        """

        return str(self.__mapper[id].getAttribute("resultType"))



#
# for SQL Clients
#

class PySQLClientSession(metaclass=ABCMeta):
    """
        An abstract class for the client session

        Author
        -------
        uxl21
    """

    @abstractmethod
    def __init__(self) -> None: ...

    @abstractmethod
    def connect(self, url:str) -> None:
        """
            Connects to the database.

            Author
            -------
            uxl21
        """
        pass

    @abstractmethod
    def selectList(self, queryId:str, parameter:dict) -> list: ...

    @abstractmethod
    def selectOne(self, queryId:str, parameter:dict=None) -> any: ...

    @abstractmethod
    def insert(self, queryId:str, parameter:dict=None) -> any: ...

    @abstractmethod
    def update(self, queryId:str, parameter:dict=None) -> any: ...

    @abstractmethod
    def delete(self, queryId:str, parameter:dict=None) -> any: ...

    @abstractmethod
    def close(self) -> None: ...






class OracleClientSession(PySQLClientSession):
    """
        The client session class for Oracle.

        Author
        -------
        uxl21
    """

    def __init__(self, sqlMapper:PySQLMapper) -> None:
        self.__sqlMapper = sqlMapper
        self.__connection = None        


    #
    # implemented
    #
    def connect(self, url:str, user:str=None, password:str=None):
        self.__connection = cx_Oracle.connect(user, password, url)


    #
    # implemented
    #
    def selectList(self, queryId:str, parameter:dict=None) -> list:
        queryString = self.__sqlMapper.getQuery(queryId, parameter)

        cursor = self.__connection.cursor()
        cursor.execute(queryString)
        
        # <select id="..." resultType="map|MAP|Map">
        if self.__sqlMapper.getResultType(queryId).upper() == "MAP":
            self.__rowTodictFactory(cursor)

        list = cursor.fetchall()

        cursor.close()

        return list


    #
    # implemented
    #
    def selectOne(self, queryId:str, parameter:dict=None) -> any:
        queryString = self.__sqlMapper.getQuery(queryId, parameter)

        cursor = self.__connection.cursor()
        cursor.execute(queryString)

        # <select id="..." resultType="map|MAP|Map">
        if self.__sqlMapper.getResultType(queryId).upper() == "MAP":
            self.__rowTodictFactory(cursor)

        one = cursor.fetchone()

        cursor.close()

        return one


    #
    # implemented
    #
    def insert(self, queryId:str, parameter:dict=None) -> any:
        return self.update(queryId, parameter)


    #
    # implemented
    #
    def update(self, queryId:str, parameter:dict=None) -> any:
        try:
            queryString = self.__sqlMapper.getQuery(queryId, parameter)

            cursor = self.__connection.cursor()
            cursor.execute(queryString)

            self.__connection.commit()

            count = cursor.rowcount

        except Error as err:
            #print(err)
            self.__connection.rollback()
            count = -1

            raise PyBatisException(err)

        finally:
            cursor.close()

        return count


    #
    # implemented
    #
    def delete(self, queryId:str, parameter:dict=None) -> any:
        return self.update(queryId, parameter)


    #
    # implemented
    #
    def close(self):
        self.__connection.close()


    def __rowTodictFactory(self, cursor):
        columns = [col[0] for col in cursor.description]
        cursor.rowfactory = lambda *args: dict(zip(columns, args))



# sqlite3
class SQLite3ClientSession(PySQLClientSession):

    def __init__(self, sqlMapper:PySQLMapper) -> None:
        self.__sqlMapper = sqlMapper
        self.__connection = None


    def connect(self, url:str, user:str=None, password:str=None):
        """
            Connects to SQLite3 database.

            Author
            -------
            uxl21
        """

        self.__connection = sqlite3.connect(url)


    #
    # implemented
    #
    def selectList(self, queryId:str, parameter:dict=None) -> list:
        queryString = self.__sqlMapper.getQuery(queryId, parameter)

        cursor = self.__connection.cursor()
        cursor.execute(queryString)
       
        # <select id="..." resultType="map|MAP|Map">
        if self.__sqlMapper.getResultType(queryId).upper() == "MAP":
            cursor.row_factory = self.__rowTodictFactory

        list = cursor.fetchall()

        cursor.close()

        return list


    #
    # implemented
    #
    def selectOne(self, queryId:str, parameter:dict=None) -> any:
        queryString = self.__sqlMapper.getQuery(queryId, parameter)

        cursor = self.__connection.cursor()
        cursor.execute(queryString)

        # <select id="..." resultType="map|MAP|Map">
        if self.__sqlMapper.getResultType(queryId).upper() == "MAP":
            cursor.row_factory = self.__rowTodictFactory


        one = cursor.fetchone()

        cursor.close()

        return one


    #
    # implemented
    #
    def insert(self, queryId:str, parameter:dict=None) -> any:
        return self.update(queryId, parameter)


    #
    # implemented
    #
    def update(self, queryId:str, parameter:dict=None) -> any:
        try:
            queryString = self.__sqlMapper.getQuery(queryId, parameter)

            cursor = self.__connection.cursor()
            cursor.execute(queryString)

            self.__connection.commit()

            count = cursor.rowcount

        except Error as err:
            #print(err)
            self.__connection.rollback()
            count = -1

            raise PyBatisException(err)

        finally:
            cursor.close()

        return count


    #
    # implemented
    #
    def delete(self, queryId:str, parameter:dict=None) -> any:
        return self.update(queryId, parameter)


    #
    # implemented
    #
    def close(self):
        self.__connection.close()


    def __rowTodictFactory(self, cursor, row):
        d = { }

        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]

        return d


# mysql
class MySQLClientSession(PySQLClientSession):

    def __init__(self, sqlMapper:PySQLMapper) -> None:
        self.__sqlMapper = sqlMapper
        self.__connection = None

    
    #
    # implemented
    #
    def connect(self, url:str, user:str=None, password:str=None, db:str=None, charset:str=None):
        self.__connection = pymysql.connect(host=url, user=user, password=password, db=db, charset=charset)

    
    #
    # implemented
    #
    def selectList(self, queryId:str, parameter:dict=None) -> list:
        queryString = self.__sqlMapper.getQuery(queryId, parameter)

        cursor = self.__connection.cursor()
        cursor.execute(queryString)
        
        #if self.__sqlMapper.getResultType(queryId).upper() == "MAP":
        #    cursor.row_factory = self.__rowTodictFactory

        list = cursor.fetchall()

        cursor.close()

        return list


    #
    # implemented
    #
    def selectOne(self, queryId:str, parameter:dict=None) -> any:
        queryString = self.__sqlMapper.getQuery(queryId, parameter)

        cursor = self.__connection.cursor()
        cursor.execute(queryString)

        #if self.__sqlMapper.getResultType(queryId).upper() == "MAP":
        #    cursor.row_factory = self.__rowTodictFactory

        one = cursor.fetchone()

        cursor.close()

        return one


    #
    # implemented
    #
    def insert(self, queryId:str, parameter:dict=None) -> any:
        return self.update(queryId, parameter)


    #
    # implemented
    #
    def update(self, queryId:str, parameter:dict=None) -> any:
        try:
            queryString = self.__sqlMapper.getQuery(queryId, parameter)

            cursor = self.__connection.cursor()
            cursor.execute(queryString)

            self.__connection.commit()

            count = cursor.rowcount

        except Error as err:
            #print(err)
            self.__connection.rollback()
            count = -1

            raise PyBatisException(err)

        finally:
            cursor.close()

        return count


    #
    # implemented
    #
    def delete(self, queryId:str, parameter:dict=None) -> any:
        return self.update(queryId, parameter)


    #
    # implemented
    #
    def close(self):
        self.__connection.close()