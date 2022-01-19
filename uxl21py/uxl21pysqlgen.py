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
from uxl21pybatis import PybatisSQLMapper, OracleClientSession


class SQLGenerator():
    
    def __init__(self) -> None:
        basePath = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        currPath = os.path.join(basePath, "./uxl21py/resources/mappers/sqlgen_sql.xml")
        print("currPath =======>>>>>>>  " + currPath)
    
        self.sqlMapper = PybatisSQLMapper(currPath)
        self.sqlClient = OracleClientSession(self.sqlMapper)
        self.sqlClient.connect(url="218.152.158.146:6837/ORCLCDB", user="SFBO", password="sfbo")
        
        
    def selectUserList(self) -> List[Dict]:
        return self.sqlClient.selectList("SQLGEN.selectUserlist")


if __name__ == "__main__":
    ## pyinstaller --onefile --add-data "./uxl21py/resources/mappers/sqlgen_sql.xml;./uxl21py/resources/mappers" ./uxl21py/uxl21pysqlgen.py
    newPath = "C:\\app\\sklee21\\product\\12.2.0\\client_3;" + os.getenv("PATH")

    os.putenv("NLS_LANG", "AMERICAN_AMERICA.UTF8")
    os.putenv("PATH", newPath)
    



    sqlGen = SQLGenerator()
    print( sqlGen.selectUserList() )
    