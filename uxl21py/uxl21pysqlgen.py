"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is a part of uxl21py

    uxl21pysqlgen.py
    
    Author
    -------
    uxl21
"""


import os
import sys
from typing import Dict, List
from uxl21py.uxl21pydata import JSONConfigData
from uxl21pybatis import PybatisSQLMapper, OracleClientSession


class SQLGenerator():
    
    def __init__(self, configPath:str) -> None:
        """
            Constructor
        """
        
        self.configData = JSONConfigData(configPath)        
        
        
        #
        # path info
        basePath = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        sqlMapperPath = os.path.join(basePath, self.configData.getConfig("sqlmapper_path"))
        oracleClientPath = self.configData.getConfig("oracle_client_path")
        
        newPath = oracleClientPath + ";" + os.getenv("PATH")
        os.putenv("PATH", newPath)
        
        
        #
        # database connection info
        address = self.configData.getConfig("address")
        port = self.configData.getConfig("port")
        sid = self.configData.getConfig("sid")
        dbUrl = address + ":" + port + "/" + sid
        
        user = self.configData.getConfig("user")
        password = self.configData.getConfig("password")
        
        
        #
        # creates mapper and SQL client
        self.sqlMapper = PybatisSQLMapper(sqlMapperPath)
        self.sqlClient = OracleClientSession(self.sqlMapper)
        self.sqlClient.connect(url=dbUrl, user=user, password=password)
        
        
    def selectUserList(self) -> List[Dict]:
        """
            Selects user list of current database.
        """
        
        return self.sqlClient.selectList("SQLGEN.selectUserlist")


## pyinstaller --onefile --add-data "./uxl21py/resources/mappers/sqlgen_sql.xml;./uxl21py/resources/mappers" ./uxl21py/uxl21pysqlgen.py
if __name__ == "__main__":
    
    
    newPath = "C:\\app\\sklee21\\product\\12.2.0\\client_3;" + os.getenv("PATH")

    os.putenv("NLS_LANG", "AMERICAN_AMERICA.UTF8")
    os.putenv("PATH", newPath)
    



    sqlGen = SQLGenerator()
    print( sqlGen.selectUserList() )
    