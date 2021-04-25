#
# Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
# 
# This file is part of OAS Generator
# 
# @author uxl21
#
import datetime
import json
import logging
import os
import sys
import yaml


from PyQt5.uic.properties import QtGui

import qtmodern.styles
import qtmodern.windows
import qdarkstyle

from abc import *
from typing import Any, Dict, List
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import *

from uxl21pybatis import PybatisSQLMapper, SQLite3ClientSession
from uxl21pyutil import *





"""
    This class defines constants for OAS application
"""
class OASConstants():
    SCHEMA_SEQ_KEY_PREFIX ="SCHEMA_SEQ_"
    PATH_SEQ_KEY_PREFIX = "PATH_SEQ_"

    THEME_QMODERN_DARK = "QMODERN_DARK"
    THEME_QMODERN_LIGHT = "QMODERN_LIGHT"
    THEME_QDARKSTYLE = "QDARKSTYLE"

    EXPORT_TYPE_REDOC = "redoc"
    EXPORT_TYPE_SWAGGER = "swagger"





#
# configuration class
#
class OASConfig():

    def __new__(cls, *args, **kwargs) -> Any:
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.__loadConfigs()

        return cls._instance 


    #
    # load configuration file
    #
    def __loadConfigs(self) -> None:
        # fixed config file
        configFile = open("./resources/oas_config.json", "r")

        # read
        jsonStr = configFile.read()
        
        # load
        self.__configData = json.loads(jsonStr)

        configFile.close()


    #
    # return config value of the specified name
    #
    def getConfig(self, configName:str) -> Any:
        return self.__configData[configName]


    #
    # return singleton instance
    #
    @staticmethod
    def getInstance():
        return OASConfig()





#
# Abstract data service class
#
class OASDataService(metaclass=ABCMeta):

    #
    # search OAS header list
    #
    @abstractmethod
    def getHeaderList(self, parameter) -> List[Dict]: ...

    #
    # search server list
    #
    @abstractmethod
    def getServerList(self, parameter) -> List[Dict]: ...

    #
    # search tag list
    #
    @abstractmethod
    def getTagList(self, parameter) -> List[Dict]: ...

    #
    # search path list
    #
    @abstractmethod
    def getPathList(self, parameter) -> List[Dict]: ...

    #
    # search path's header list
    #
    @abstractmethod
    def getPathHeaderList(self, parameter) -> List[Dict]: ...

    #
    # search path's response list
    #
    @abstractmethod
    def getPathResponseList(self, parameter) -> List[Dict]: ...

    #
    # search schema list
    #
    @abstractmethod
    def getSchemaList(self, parameter) -> List[Dict]: ...

    #
    # search schema's property list
    #
    @abstractmethod
    def getSchemaPropList(self, parameter) -> List[Dict]: ...

    #
    # save OAS header information
    #
    @abstractmethod
    def saveHeader(self, parameter) -> int: ...

    #
    # save server list
    #
    @abstractmethod
    def saveServers(self, parameter, serverList) -> int: ...

    #
    # save tag list
    #
    @abstractmethod
    def saveTags(self, parameter, tagList) -> int: ...

    #
    # save path list
    #
    @abstractmethod
    def savePaths(self, parameter, pathList) -> int: ...

    #
    # save path's header list
    #
    @abstractmethod
    def savePathHeaders(self, parameter, pathHeaderList) -> int: ...


    #
    # save path's response list
    #
    @abstractmethod
    def savePathResponses(self, parameter, pathResponseList) -> int: ...

    #
    # save schema list
    #
    @abstractmethod
    def saveSchemas(self, parameter, schemaList) -> int: ...

    #
    # save schema's property list
    #
    @abstractmethod    
    def saveSchemaProps(self, parameter, schemaPropList) -> int: ...





#
# Data service class
#
class OASSQLite3DataService(OASDataService):

    def __new__(cls, *args, **kwargs) -> Any:
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            cls._instance.__initialize()

        return cls._instance 


    #
    # return singleton instance
    #
    @staticmethod
    def getInstance():
        return OASSQLite3DataService()


    #
    # initialize
    #
    def __initialize(self) -> None:
        oasConfig = OASConfig.getInstance()

        self.sqlMapper = PybatisSQLMapper(oasConfig.getConfig("sqlmapper_path"))
        self.sqlClient = SQLite3ClientSession(self.sqlMapper)
        self.sqlClient.connect(oasConfig.getConfig("dbfile_path"))
    

    #
    # search OAS header list
    #
    def getHeaderList(self, parameter) -> List[Dict]:
        return self.sqlClient.selectList("OAS.selectHeaderList", parameter)


    #
    # search server list
    #
    def getServerList(self, parameter) -> List[Dict]:
        return self.sqlClient.selectList("OAS.selectServerList", parameter)


    #
    # search tag list
    #
    def getTagList(self, parameter) -> List[Dict]:
        return self.sqlClient.selectList("OAS.selectTagList", parameter)


    #
    # search path list
    #
    def getPathList(self, parameter) -> List[Dict]:
        return self.sqlClient.selectList("OAS.selectPathList", parameter)


    #
    # search path's header list
    #
    def getPathHeaderList(self, parameter) -> List[Dict]:
        return self.sqlClient.selectList("OAS.selectPathHeaderList", parameter)


    #
    # search path's response list
    #
    def getPathResponseList(self, parameter) -> List[Dict]:
        return self.sqlClient.selectList("OAS.selectPathResponseList", parameter)


    #
    # search schema list
    #
    def getSchemaList(self, parameter) -> List[Dict]:
        return self.sqlClient.selectList("OAS.selectSchemaList", parameter)


    #
    # search schema's property list
    #
    def getSchemaPropList(self, parameter) -> List[Dict]:
        return self.sqlClient.selectList("OAS.selectSchemaPropList", parameter)


    #
    # save OAS header information
    #
    def saveHeader(self, parameter) -> int:
        headerList = self.getHeaderList(parameter)

        if DataUtil.isNotEmpty(headerList):
            return self.sqlClient.update("OAS.updateHeader", parameter)
        else:
            return self.sqlClient.insert("OAS.insertHeader", parameter)


    #
    # save server list
    #
    def saveServers(self, parameter, serverList) -> int:
        self.sqlClient.delete("OAS.deleteServer", parameter)

        saveCount = 0

        for server in serverList: 
            saveCount += self.sqlClient.insert("OAS.insertServer", server)

        return saveCount


    #
    # save tag list
    #
    def saveTags(self, parameter, tagList) -> int:
        self.sqlClient.delete("OAS.deleteTag", parameter)

        saveCount = 0

        for tag in tagList:
            saveCount += self.sqlClient.insert("OAS.insertTag", tag)

        return saveCount


    #
    # save path list
    #
    def savePaths(self, parameter, pathList) -> int:
        self.sqlClient.delete("OAS.deletePath", parameter)

        saveCount = 0

        for path in pathList:
            saveCount += self.sqlClient.insert("OAS.insertPath", path)

        return saveCount


    #
    # save path's header list
    #
    def savePathHeaders(self, parameter, pathHeaderList) -> int:
        self.sqlClient.delete("OAS.deletePathHeader", parameter)

        saveCount = 0

        for header in pathHeaderList:
            saveCount += self.sqlClient.insert("OAS.insertPathHeader", header)

        return saveCount


    #
    # save path's response list
    #
    def savePathResponses(self, parameter, pathResponseList) -> int:
        self.sqlClient.delete("OAS.deletePathResponse", parameter)

        saveCount = 0

        for response in pathResponseList:
            saveCount += self.sqlClient.insert("OAS.insertPathResponse", response)

        return saveCount


    #
    # save schema list
    #
    def saveSchemas(self, parameter, schemaList) -> int:
        self.sqlClient.delete("OAS.deleteSchema", parameter)

        saveCount = 0

        for schema in schemaList:
            saveCount += self.sqlClient.insert("OAS.insertSchema", schema)

        return saveCount


    #
    # save schema's property list
    #
    def saveSchemaProps(self, parameter, schemaPropList) -> int:
        self.sqlClient.delete("OAS.deleteSchemaProp", parameter)

        saveCount = 0

        for schemaProp in schemaPropList:
            saveCount += self.sqlClient.insert("OAS.insertSchemaProp", schemaProp)

        return saveCount





#
# OAS Document builder class
#
class OASDocumentBuilder():
    
    #
    # Constructor
    #
    def __init__(self):
        self.__header = {}
        self.__servers = None
        self.__tags = None
        self.__paths = None
        self.__pathHeaders = None
        self.__pathResponses = None
        self.__schemas = None


    #
    # set header data
    #
    def setHeader(self, header:Dict) -> None:
        self.__header = header


    #
    # set server list data
    #
    def setServers(self, servers:List) -> None:
        self.__servers = servers


    #
    # set tag list data
    #
    def setTags(self, tags:List) -> None:
        self.__tags = tags


    #
    # set path data
    #
    def setPaths(self, paths:List, pathHeaders:Dict, pathResponses:Dict) -> None:
        self.__paths = paths
        self.__pathHeaders = pathHeaders
        self.__pathResponses = pathResponses


    #
    # set schema data
    #
    def setSchemas(self, schemas:List, schemaProperties:Dict) -> None:
        self.__schemas = schemas
        self.__schemaProperties = schemaProperties


    #
    # build data as dictionary object
    # 
    def build(self) -> dict:
        # header
        oasData = {
            "openapi": "3.0.0",
            "info": {
                "description": self.__header.get("DESCRIPTION"),
                "version": self.__header.get("VERSION"),
                "title": self.__header.get("TITLE"),
                "termsOfService": self.__header.get("TERMS_OF_SERVICE"),
                "contact": {
                    "name": self.__header.get("CONTACT_NAME"),
                    "email": self.__header.get("CONTACT_EMAIL")
                }
            },
            "externalDocs": {
                "url": self.__header.get("EXT_DOCS_URL"),
                "description": self.__header.get("EXT_DOCS_DESC")                
            },
            "servers": [],
            "tags": [],
            "paths": {}
        }

        # servers
        for server in self.__servers:
            oasData["servers"].append({
                "url": server.get("URL"),
                "description": server.get("DESCRIPTION")
            })
        
        # tags
        for tag in self.__tags:
            oasData["tags"].append({
                "name": tag.get("NAME"),
                "description": tag.get("DESCRIPTION")
            })

        # paths
        for path in self.__paths:
            pathValue = path.get("PATH")
            methodValue = path.get("METHOD")
            reqBodyContentTypeValue = path.get("REQUEST_BODY_CONTENT_TYPE")

            oasData["paths"][pathValue] = {
                methodValue: {
                    "tags": [
                        path.get("TAG_SEQ")
                    ],
                    "summary": path.get("SUMMARY"),
                    "description": path.get("DESCRIPTION"),
                    "operationId": path.get("OPERATION_ID"),
                    "requestBody": {
                        "content": {
                            reqBodyContentTypeValue: {
                                "schema": {
                                    "$ref": "#/components/schemas/" + path.get("REQUEST_BODY_SCHEMA_SEQ")
                                }
                            }
                        }
                    },
                    "responses": {}
                }
            }

            # headers for paths
            pathHeaders = self.__pathHeaders[OASConstants.PATH_SEQ_KEY_PREFIX + str(path.get("PATH_SEQ"))]

            if DataUtil.isNotEmpty(pathHeaders):
                parametersArr = []

                for header in pathHeaders:
                    parametersArr.append({
                        "name": header.get("NAME"),
                        "in": "header",
                        "required": DictUtil.getBoolean(header, "REQUIRED"),
                        "schema": {
                            "type": header.get("TYPE")
                        },
                        "description": header.get("DESCRIPTION")
                    })
                
                if DataUtil.isNotEmpty(parametersArr):
                    oasData["paths"][pathValue][methodValue]["parameters"] = parametersArr

            # responses for paths
            responses = self.__pathResponses[OASConstants.PATH_SEQ_KEY_PREFIX + str(path.get("PATH_SEQ"))]

            for response in responses:
                contentTypeValue = response.get("CONTENT_TYPE")
                schemaValue = response.get("SCHEMA_SEQ")
                statusCdValue = response.get("STATUS_CD")                
                statusObj = {
                    "description": response.get("DESCRIPTION")
                }

                if DataUtil.isNotEmpty(contentTypeValue):
                    contentObj = {}
                    contentObj[contentTypeValue] = {}

                    if DataUtil.isNotEmpty(schemaValue):
                        contentObj[contentTypeValue]["schema"] = {
                            "$ref": "#/components/schemas/" + schemaValue
                        }
                    statusObj["content"] = contentObj
                
                oasData["paths"][pathValue][methodValue]["responses"][statusCdValue] = statusObj

            # schemas
            if DataUtil.isNotEmpty(self.__schemas):
                oasData["components"] = {
                    "schemas": {}
                }

                for schema in self.__schemas:
                    schemaProps = self.__schemaProperties.get(OASConstants.SCHEMA_SEQ_KEY_PREFIX + str(schema.get("SCHEMA_SEQ")))
                    schemaNameValue = schema.get("NAME")
                    schemaObj = {
                        "type": schema.get("TYPE")
                    }

                    if DataUtil.isNotEmpty(schemaProps):
                        schemaPropsObj = {}
                        requiredProps = []

                        for schemaProp in schemaProps:
                            typeValue = schemaProp.get("TYPE")
                            nameValue = schemaProp.get("NAME")

                            if DataUtil.toBoolean(schemaProp.get("REQUIRED")):
                                requiredProps.append(nameValue)

                            schemaPropsObj[nameValue] = {
                                "type": typeValue,
                                "description": schemaProp.get("DESCRIPTION")
                            }

                            # if type is 'array', VALUE field will be 'items.enum' and REF_SCHEMA_SEQ field will be 'items.$ref'.
                            # REF_SCHEMA_SEQ has priority.
                            if typeValue == "array":
                                refSchemaSeqValue = schemaProp.get("REF_SCHEMA_SEQ")

                                if DataUtil.isNotEmpty(refSchemaSeqValue):
                                    schemaPropsObj[nameValue]["items"] = {
                                        "$ref": "#/components/schemas/" + refSchemaSeqValue
                                    }

                                else:
                                    valValue = schemaProp.get("VALUE")
                                    
                                    if DataUtil.isNotEmpty(valValue):
                                        enumValues = str(valValue).split(",")

                                        schemaPropsObj[nameValue]["items"] = {
                                            "enum": enumValues
                                        }
                        oasData["components"]["schemas"][schemaNameValue] = schemaObj
                        oasData["components"]["schemas"][schemaNameValue]["properties"] = schemaPropsObj
                    # end of schema property loop

                    if DataUtil.isNotEmpty(requiredProps):
                        oasData["components"]["schemas"][schemaNameValue]["required"] = requiredProps

                # end of schema loop

        return oasData


    #
    # generate JSON or YAML file
    #
    def generateDataFile(self, oasData:dict, dir:str, apiID:str) -> bool:
        try:
            exportType = DataUtil.nvl(OASConfig.getInstance().getConfig("export_type"), OASConstants.EXPORT_TYPE_REDOC).lower()
            fileExt = DataUtil.decode(exportType, OASConstants.EXPORT_TYPE_REDOC, ".json", ".yaml")
            strData = DataUtil.decode(exportType, OASConstants.EXPORT_TYPE_REDOC, json.dump(oasData), yaml.dump(oasData))

            # save as file
            with open(dir + os.sep + apiID + fileExt, "w") as dataFile:
                dataFile.write(strData)

        except Exception as ex:
            logging.getLogger().exception(ex)
            return False

        return True


    #
    # generate data file and HTML
    #
    def generateAPIDoc(self, oasData:dict, title:str, dir:str, apiID:str) -> bool:
        try:
            exportType = DataUtil.nvl(OASConfig.getInstance().getConfig("export_type"), OASConstants.EXPORT_TYPE_REDOC).lower()
            fileExt = DataUtil.decode(exportType, OASConstants.EXPORT_TYPE_REDOC, ".json", ".yaml")
            dataContent = DataUtil.decode(exportType, OASConstants.EXPORT_TYPE_REDOC, json.dumps(oasData), yaml.dump(oasData))

            # save data file
            fileName = dir + os.sep + apiID

            with open(fileName + fileExt, "w") as dataFile:
                dataFile.write(dataContent)

            # template
            templateFile = OASConfig.getInstance().getConfig(exportType + "_template")
            templateLines = None

            with open(templateFile, "r") as templateFile:
                templateLines = templateFile.readlines()

            if DataUtil.isEmpty(templateLines):
                return False

            # save template content with title and datefile as html file
            templateContent = ""

            for oneLine in templateLines:
                templateContent += oneLine

            templateContent = templateContent.replace("#{TITLE}", title).replace("#{DATAFILE}", apiID + fileExt)

            with open(fileName + ".html", "w") as htmlFile:
                htmlFile.write(templateContent)

        except Exception as ex:
            logging.getLogger().exception(ex)
            return False

        return True





#
# OAS GUI
#

# main window
class OASMainWindow(QMainWindow, uic.loadUiType(OASConfig.getInstance().getConfig("ui_main_path"))[0]):

    #
    # Constructor
    #
    def __init__(self, oasDataService:OASDataService) -> None:
        super().__init__()

        self.oasDataService = oasDataService

        # initialize data
        self.oasChildTabWidgets = []

        # initialize UI components
        self.setupUi(self)
        self.initUI()

        # initialize flags
        self.theme = OASConstants.THEME_QMODERN_DARK


    #
    # initialize GUI components
    #
    def initUI(self) -> None:
        #
        # tabs
        # list tab
        childTabWidget = OASTabChildWidgets.OASListWidget(self)
        childTabWidget.setDataService(self.oasDataService)
        self.oasChildTabWidgets.append(childTabWidget)
        vbox = QVBoxLayout()
        vbox.addWidget(childTabWidget)
        self.tab_container.widget(0).setLayout(vbox)
        
        # header tab
        childTabWidget = OASTabChildWidgets.OASHeaderWidget(self)
        childTabWidget.setDataService(self.oasDataService)
        self.oasChildTabWidgets.append(childTabWidget)
        vbox = QVBoxLayout()
        vbox.addWidget(childTabWidget)
        self.tab_container.widget(1).setLayout(vbox)

        # paths tab
        childTabWidget = OASTabChildWidgets.OASPathsWidget(self)
        childTabWidget.setDataService(self.oasDataService)
        self.oasChildTabWidgets.append(childTabWidget)
        vbox = QVBoxLayout()
        vbox.addWidget(childTabWidget)
        self.tab_container.widget(2).setLayout(vbox)

        # schema tab
        childTabWidget = OASTabChildWidgets.OASSchemasWidget(self)
        childTabWidget.setDataService(self.oasDataService)
        self.oasChildTabWidgets.append(childTabWidget)
        vbox = QVBoxLayout()
        vbox.addWidget(childTabWidget)
        self.tab_container.widget(3).setLayout(vbox)

        #self.setCentralWidget(self.tab_container)
        self.setFixedSize(QtCore.QSize(1024, 768))

        #
        # menu
        # actions for file menu
        exportAction = QAction("Export", self)
        exportAction.setShortcut("Ctrl+E")
        exportAction.setStatusTip("Export data to Document")
        exportAction.triggered.connect(self.export)

        #saveAction = QAction(QIcon("./images/save.png"), "Save", self)
        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Save data")
        saveAction.triggered.connect(self.saveData)

        #exitAction = QAction(QIcon("./images/exit.png"), "Exit", self)
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit application")
        exitAction.triggered.connect(qApp.quit)

        # actions for view menu
        themeActinGroup = QActionGroup(self)
        themeActinGroup.setExclusionPolicy(QActionGroup.ExclusionPolicy.Exclusive)

        qModernDarkThemeAction = QAction("QModern Dark", self)
        qModernDarkThemeAction.setCheckable(True)
        qModernDarkThemeAction.setActionGroup(themeActinGroup)
        qModernDarkThemeAction.setChecked(True)
        qModernDarkThemeAction.setStatusTip("Change theme to QModern Dark")
        qModernDarkThemeAction.triggered.connect(self.qModernDarkThemeAction_triggeredHandler)

        qModernLightThemeAction = QAction("QModern Light", self)
        qModernLightThemeAction.setCheckable(True)
        qModernLightThemeAction.setActionGroup(themeActinGroup)
        qModernLightThemeAction.setStatusTip("Change theme to QModern Light")
        qModernLightThemeAction.triggered.connect(self.qModernLightThemeAction_triggeredHandler)

        qDarkStyleThemeAction = QAction("QDark Style", self)
        qDarkStyleThemeAction.setCheckable(True)
        qDarkStyleThemeAction.setActionGroup(themeActinGroup)
        qDarkStyleThemeAction.setStatusTip("Change theme to QDark style")
        qDarkStyleThemeAction.triggered.connect(self.qDarkStyleThemeAction_triggeredHandler)

        # actions for help menu
        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(self.aboutAction_triggeredHandler)


        # menu bar
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)

        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(exportAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        viewMenu = menuBar.addMenu("&View")
        themeMenu = viewMenu.addMenu("Theme")
        themeMenu.addAction(qModernDarkThemeAction)
        themeMenu.addAction(qModernLightThemeAction)
        #themeMenu.addAction(qDarkStyleThemeAction)

        helpMenu = menuBar.addMenu("Help")
        helpMenu.addAction(aboutAction)


    #
    # keyRelease event handler
    #
    def keyReleaseEvent(self, event:QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_F5:
            self.oasChildTabWidgets[0].searchList()


    #
    # triggered handler for QModern dark action
    #
    def qModernDarkThemeAction_triggeredHandler(self) -> None:
        if self.theme != OASConstants.THEME_QMODERN_DARK:
            qtmodern.styles.dark(QApplication.instance())
            self.theme = OASConstants.THEME_QMODERN_DARK


    #
    # triggered handler for QModern light action
    #
    def qModernLightThemeAction_triggeredHandler(self) -> None:
        if self.theme != OASConstants.THEME_QMODERN_LIGHT:
            qtmodern.styles.light(QApplication.instance())
            self.theme = OASConstants.THEME_QMODERN_LIGHT


    #
    # triggered handler for QDark style action
    #
    def qDarkStyleThemeAction_triggeredHandler(self) -> None:
        if self.theme != OASConstants.THEME_QDARKSTYLE:
            QApplication.instance().setStyleSheet(qdarkstyle.load_stylesheet())
            self.theme = OASConstants.THEME_QDARKSTYLE


    #
    # triggered handler for Help>About action
    #
    def aboutAction_triggeredHandler(self) -> None:
        aboutText = """
            OpenAPI Specification Document Generator

            Version: 1.0.0
            OpenAPI Version: 3.0.0
            Powered by Swagger and Redoc

            Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
        """
        QMessageBox.information(self, "OAS Generator", aboutText)


    #
    # set data to all child tabs
    #
    def setTabData(self, data) -> None:
        for childTab in self.oasChildTabWidgets:
            childTab.setData(data)
        
    
    #
    # select the specified tab by index
    #
    def selectTab(self, index) -> None:
        self.tab_container.setCurrentIndex(index)


    #
    # export current OAS data
    #
    def export(self) -> None:
        # 1. check header
        headerInfoMap = self.oasChildTabWidgets[1].getData()
        header = headerInfoMap.get("headerData")
                
        if DataUtil.isAnyEmpty(header):
            QMessageBox.warning(self, "", "Select the OAS header to export!")
            return

        # 2. get user input
        apiId, okClicked = QInputDialog.getText(self, "", 'Enter API ID')

        if DataUtil.isEmpty(apiId) or not okClicked:
            return

        dirToSave = QFileDialog.getExistingDirectory(self, "Select directory to save")

        if DataUtil.isEmpty(dirToSave):
            return

        # 3. show progress
        self.progressDialog = QWidgetUtil.createProgressDialog(title="PLZ wait", label="In progress...", maximum=80)
        self.progressDialog.show()

        QApplication.processEvents()

        # 4. collect data
        servers = headerInfoMap.get("serverList")
        tags = headerInfoMap.get("tagList")
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 10

        pathInfoMap = self.oasChildTabWidgets[2].getData()
        paths = pathInfoMap.get("pathList")
        pathHeaders = pathInfoMap.get("pathHeaderListMap")
        pathResponses = pathInfoMap.get("pathResponseListMap")
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 20

        schemaInfoMap = self.oasChildTabWidgets[3].getData()
        schemas = schemaInfoMap.get("schemaList")
        schemaProps = schemaInfoMap.get("propertyListMap")
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 30
        
        # 5. start to export
        docBuilder = OASDocumentBuilder()
        docBuilder.setHeader(header)
        docBuilder.setServers(servers)
        docBuilder.setTags(tags)
        docBuilder.setPaths(paths, pathHeaders, pathResponses)
        docBuilder.setSchemas(schemas, schemaProps)
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 40
        
        dataObj = docBuilder.build()
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 50
        result = docBuilder.generateAPIDoc(dataObj, header.get("TITLE"), dirToSave, apiId)
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 60

        self.progressDialog.close()
        
        # 6. show result
        resultMessage = None

        if result:
            resultMessage = "Export successfully!"
            QMessageBox.information(self, "", resultMessage)
        else:
            resultMessage = "Failed to generate!"
            QMessageBox.warning(self, "", resultMessage)

        self.statusBar().showMessage(resultMessage)


    #
    # clear all data
    #
    def clear(self) -> None:
        for childTabWidget in self.oasChildTabWidgets:
            childTabWidget.clear()


    #
    # save current data
    #
    def saveData(self) -> None:
        # 1. check
        checkData = self.oasChildTabWidgets[0].getData()

        if not DictUtil.getBoolean(checkData, "headerSelected"):
            QMessageBox.warning(self, "", "Select the OAS header first!")
            return

        # 0. show progress
        self.progressDialog = QWidgetUtil.createProgressDialog(80)
        self.progressDialog.show()

        QApplication.processEvents()
            
        # 2. save header information
        headerInfoMap = self.oasChildTabWidgets[1].getData()

        # 2.1. header
        headerData = headerInfoMap.get("headerData")
        resultCount = self.oasDataService.saveHeader(headerData)

        if resultCount == -1:
            QMessageBox.critical(self, "Error", "Failed to save header")
            self.statusBar().showMessage("Failed to save header")
            return
            
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 10

        # 2.2. servers
        serverList = headerInfoMap.get("serverList")
        resultCount = self.oasDataService.saveServers(headerData, serverList)

        if resultCount == -1:
            QMessageBox.critical(self, "Error", "Failed to save servers")
            self.statusBar().showMessage("Failed to save servers")
            return
            
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 20

        # 2.3. tags
        tagList = headerInfoMap.get("tagList")
        resultCount = self.oasDataService.saveTags(headerData, tagList)

        if resultCount == -1:
            QMessageBox.critical(self, "Error", "Failed to save tags")
            self.statusBar().showMessage("Failed to save tags")
            return
            
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 30

        # 2.4. paths
        pathInfoMap = self.oasChildTabWidgets[2].getData()
        pathList = pathInfoMap.get("pathList")
        resultCount = self.oasDataService.savePaths(headerData, pathList)

        if resultCount == -1:
            QMessageBox.critical(self, "Error", "Failed to save paths")
            self.statusBar().showMessage("Failed to save paths")
            return
            
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 40

        # 2.5. headers
        pathHeaderListMap = pathInfoMap.get("pathHeaderListMap")
        pathHeaderList = []
        
        for key in pathHeaderListMap:
            for pathHeader in pathHeaderListMap[key]:
                pathHeaderList.append(pathHeader)

        resultCount = self.oasDataService.savePathHeaders(headerData, pathHeaderList)

        if resultCount == -1:
            QMessageBox.critical(self, "Error", "Failed to save headers")
            self.statusBar().showMessage("Failed to save headers")
            return
            
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 50

        # 2.6. responses
        pathResponseListMap = pathInfoMap.get("pathResponseListMap")
        pathResponseList = []
        
        for key in pathResponseListMap:
            for pathHeader in pathResponseListMap[key]:
                pathResponseList.append(pathHeader)

        resultCount = self.oasDataService.savePathResponses(headerData, pathResponseList)

        if resultCount == -1:
            QMessageBox.critical(self, "Error", "Failed to save responses")
            self.statusBar().showMessage("Failed to save responses")
            return
            
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 60

        # 2.7. schemas
        schemaInfoMap = self.oasChildTabWidgets[3].getData()
        schemaList = schemaInfoMap.get("schemaList")
        resultCount = self.oasDataService.saveSchemas(headerData, schemaList)

        if resultCount == -1:
            QMessageBox.critical(self, "Error", "Failed to save schemas")
            self.statusBar().showMessage("Failed to save schemas")
            return
            
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 70

        # 2.8. schema's properties
        propertyListMap = schemaInfoMap.get("propertyListMap")
        pathResponseList = []
        
        for key in propertyListMap:
            for pathHeader in propertyListMap[key]:
                pathResponseList.append(pathHeader)

        resultCount = self.oasDataService.saveSchemaProps(headerData, pathResponseList)

        if resultCount == -1:
            QMessageBox.critical(self, "Error", "Failed to save schema properties")
            self.statusBar().showMessage("Failed to save schema properties")
            return
            
        self.progressDialog.setValue(self.progressDialog.value() + 10)  # value = 80
        self.progressDialog.close()

        # show result message
        QMessageBox.information(self, "", "Save data sucessfully")
        self.statusBar().showMessage("Save data sucessfully")
        self.oasChildTabWidgets[0].updateOasListData()





#
# Abstract class for child tabs
#
class AbstactOASTabChildWidget(QWidget):

    #
    # set DataService instance
    #
    def setDataService(self, oasDataService:OASDataService) -> None:
        self.oasDataService = oasDataService
    

    @abstractmethod
    def setData(self, data) -> None: ...

    @abstractmethod
    def getData(self) -> Dict: ...

    @abstractmethod
    def clear(self) -> None: ...





#
# concrete classes for child tabs
#
class OASTabChildWidgets():

    #
    # tab0 - Header list
    #
    class OASListWidget(AbstactOASTabChildWidget, uic.loadUiType(OASConfig.getInstance().getConfig("ui_list_path"))[0]):

        #
        # Constructor
        #
        def __init__(self, mainWindow:OASMainWindow) -> None:
            super().__init__()

            self.__mainWindow = mainWindow
            
            # initialize data
            self.oasList = None

            # initialize flag
            self.headerSelected = False

            # initialize UI components
            self.setupUi(self)
            self.initUI()
            

        #
        # initialize GUI components
        #
        def initUI(self) -> None:
            self.tbl_oasList.setHorizontalHeaderLabels([ "Title" ])
            self.tbl_oasList.itemDoubleClicked.connect(self.tblList_itemDoubleClickedHandler)
            
            self.btn_addNewOas.clicked.connect(self.btnAddNewOas_clickedHandler)
            self.btn_removeOas.clicked.connect(self.btnRemoveOas_clickedHandler)
            self.btn_search.clicked.connect(self.btnSearch_clickedHandler)


        #
        # itemDoubleClicked handler for OAS list
        #
        def tblList_itemDoubleClickedHandler(self, item:QTableWidgetItem) -> None:
            self.__mainWindow.setTabData(self.oasList[item.row()])
            self.__mainWindow.selectTab(1)

            self.headerSelected = True


        #
        # clicked handler for search button
        #
        def btnSearch_clickedHandler(self) -> None:
            self.searchList()


        #
        # clicked handler for add new button
        #
        def btnAddNewOas_clickedHandler(self) -> None:
            if DataUtil.isEmpty(self.oasList):
                self.oasList = []

            newOasData = {
                "UID": datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:17],
                "TITLE": "New OAS",
                "VERSION": "",
                "DESCRIPTION": "",
                "TERMS_OF_SERVICE": "",
                "CONTACT_NAME": "",
                "CONTACT_EMAIL": "",
                "EXT_DOCS_URL": "",
                "EXT_DOCS_DESC": "",
            }

            self.oasList.append(newOasData)
            self.updateOasListData()
            self.tbl_oasList.selectRow(len(self.oasList) - 1)

            self.__mainWindow.clear()


        #
        # clicked handler for remove button
        #
        def btnRemoveOas_clickedHandler(self) -> None:
            currentRow = self.tbl_oasList.currentRow()
            
            if currentRow > -1:
                # remove from list
                self.oasList.pop(currentRow)
                self.updateOasListData()

            self.__mainWindow.clear()


        #
        # search list
        #
        def searchList(self) -> None:
            if DataUtil.isNotEmpty(self.oasList):
                self.oasList.clear()

            self.oasList = self.oasDataService.getHeaderList({"UID": ""})
            self.updateOasListData()

            self.headerSelected = False


        #
        # bind current data to table
        #
        def updateOasListData(self) -> None:
            rowCount = len(self.oasList)
            self.tbl_oasList.setRowCount(rowCount)

            for index in range(rowCount):
                self.tbl_oasList.setItem(index, 0, QTableWidgetItem(self.oasList[index]["TITLE"]))

            self.tbl_oasList.resizeColumnsToContents()
            self.tbl_oasList.resizeRowsToContents()


        #
        # implemented
        #
        def setData(self, data) -> None:
            pass


        #
        # implemented
        # get data
        #
        def getData(self) -> Dict:
            return {
                "headerSelected": self.headerSelected
            }

        
        #
        # implemented
        # clear data
        #
        def clear(self) -> None:
            pass



    #
    # tab1 - Header information
    #
    class OASHeaderWidget(AbstactOASTabChildWidget, uic.loadUiType(OASConfig.getInstance().getConfig("ui_header_path"))[0]):

        #
        # Constructor
        #
        def __init__(self, mainWindow:OASMainWindow) -> None:
            super().__init__()

            self.__mainWindow = mainWindow

            # initialize data
            self.headerData = None
            self.tagList = None
            self.serverList = None

            # initialize UI components
            self.setupUi(self)
            self.initUI()
            self.edits = {
                "TITLE": self.edt_title,
                "VERSION": self.edt_version,
                "TERMS_OF_SERVICE": self.edt_tos,
                "CONTACT_NAME": self.edt_contactName,
                "CONTACT_EMAIL": self.edt_contactEmail,
                "EXT_DOCS_URL": self.edt_extDocDesc,
                "EXT_DOCS_DESC": self.edt_extDocUrl,
                "DESCRIPTION": self.edt_description
            }


        #
        # initialize GUI components
        #
        def initUI(self) -> None:
            # initialize table
            self.tbl_serverList.setHorizontalHeaderLabels([ "URL", "DESCRIPTION" ])
            self.tbl_tagList.setHorizontalHeaderLabels([ "Name", "Description" ])

            # add/remove button for servers
            self.btn_addNewServer.clicked.connect(self.btnAddNewServer_clickedHandler)
            self.btn_removeServer.clicked.connect(self.btnRemoveServer_clickedHandler)

            # add/remove button for tags
            self.btn_addNewTag.clicked.connect(self.btnAddNewTag_clickedHandler)
            self.btn_removeTag.clicked.connect(self.btnRemoveTag_clickedHandler)

            # tables
            self.tbl_serverList.itemChanged.connect(self.tblServerList_itemChanged)
            self.tbl_serverList.keyReleaseEvent = self.tblServerList_keyReleaseEvent

            self.tbl_tagList.itemChanged.connect(self.tblTagList_itemChanged)
            self.tbl_tagList.keyReleaseEvent = self.tblTagList_keyReleaseEvent


        #
        # keyReleaseEvent handler for server table
        #
        def tblServerList_keyReleaseEvent(self, event:QKeyEvent) -> None:
            keyCode = event.key()

            if keyCode == QtCore.Qt.Key_Insert:
                self.btnAddNewServer_clickedHandler()


        #
        # keyReleaseEvent handler for tag table
        #
        def tblTagList_keyReleaseEvent(self, event:QKeyEvent) -> None:
            keyCode = event.key()

            if keyCode == QtCore.Qt.Key_Insert:
                self.btnAddNewTag_clickedHandler()


        #
        # clicked handler for add new server button
        #
        def btnAddNewServer_clickedHandler(self) -> None:
            newItem = {
                "UID": self.headerData["UID"],
                "SEQ": -1,
                "URL": "",
                "DESCRIPTION": ""
            }
            self.serverList.append(newItem)
            self.updateServerData()
            
            # select row and start to edit first cell
            lastRowIndex = len(self.serverList) - 1

            self.tbl_serverList.selectRow(lastRowIndex)
            self.tbl_serverList.editItem(self.tbl_serverList.item(lastRowIndex, 0))


        #
        # clicked handler for remove server button
        #
        def btnRemoveServer_clickedHandler(self) -> None:
            currentRow = self.tbl_serverList.currentRow()
            
            if currentRow > -1:
                # remove from list
                self.serverList.pop(currentRow)
                self.updateServerData()


        #
        # clicked handler for add new tag button
        #
        def btnAddNewTag_clickedHandler(self) -> None:
            newItem = {
                "UID": self.headerData["UID"],
                "TAG_SEQ": -1,
                "NAME": "",
                "DESCRIPTION": ""
            }
            self.tagList.append(newItem)
            self.updateTagData()

            # select row and start to edit first cell
            lastRowIndex = len(self.tagList) - 1

            self.tbl_tagList.selectRow(lastRowIndex)
            self.tbl_tagList.editItem(self.tbl_tagList.item(lastRowIndex, 0))


        #
        # clicked handler for remove tag button
        #
        def btnRemoveTag_clickedHandler(self) -> None:
            currentRow = self.tbl_tagList.currentRow()
            
            if currentRow > -1:
                # remove from list
                self.tagList.pop(currentRow)
                self.updateTagData()


        #
        # itemChanged handler for server table
        #
        def tblServerList_itemChanged(self, changedItem:QTableWidgetItem) -> None:
            self.commitServerData(changedItem)
            self.updateServerTableToContents()


        #
        # itemChanged handler for tag table
        #
        def tblTagList_itemChanged(self, changedItem:QTableWidgetItem) -> None:
            self.commitTagData(changedItem)
            self.updateTagTableToContents()


        #
        # update server table to it's contents
        #
        def updateServerTableToContents(self) -> None:
            self.tbl_serverList.resizeColumnsToContents()
            self.tbl_serverList.resizeRowsToContents()


        #
        # update tag table to it's contents
        #
        def updateTagTableToContents(self) -> None:
            self.tbl_tagList.resizeColumnsToContents()
            self.tbl_tagList.resizeRowsToContents()


        #
        # search OAS server list
        #
        def searchServerList(self, param) -> None:
            if DataUtil.isNotEmpty(self.serverList):
                self.serverList.clear()

            self.serverList = self.oasDataService.getServerList(parameter=param)
            self.updateServerData()
            self.updateServerTableToContents()

            if len(self.serverList) > 0:
                self.tbl_serverList.selectRow(0)


        #
        # search OAS tag list
        #
        def searchTagList(self, param) -> None:
            if DataUtil.isNotEmpty(self.tagList):
                self.tagList.clear()

            self.tagList = self.oasDataService.getTagList(parameter=param)
            self.updateTagData()
            self.updateTagTableToContents()

            if len(self.tagList) > 0:
                self.tbl_tagList.selectRow(0)


        #
        # bind current data to server table
        #
        def updateServerData(self) -> None:
            rowCount = len(self.serverList)
            
            self.tbl_serverList.clearContents()
            self.tbl_serverList.setRowCount(rowCount)

            for index in range(rowCount):
                self.tbl_serverList.setItem(index, 0, QTableWidgetItem(self.serverList[index]["URL"]))
                self.tbl_serverList.setItem(index, 1, QTableWidgetItem(self.serverList[index]["DESCRIPTION"]))

            self.tbl_serverList.selectRow(len(self.serverList) - 1)

        
        #
        # bind current data to tag table
        #
        def updateTagData(self) -> None:
            rowCount = len(self.tagList)
            
            self.tbl_tagList.clearContents()
            self.tbl_tagList.setRowCount(rowCount)

            for index in range(rowCount):
                self.tbl_tagList.setItem(index, 0, QTableWidgetItem(self.tagList[index]["NAME"]))
                self.tbl_tagList.setItem(index, 1, QTableWidgetItem(self.tagList[index]["DESCRIPTION"]))

            self.tbl_tagList.selectRow(len(self.tagList) - 1)


        #
        # commit header data to list
        #
        def commitHeaderData(self) -> None:
            # header data
            if self.headerData == None:
                self.headerData = {}

            for editName in self.edits:
                value = ""

                if type(self.edits[editName]) is QTextEdit:
                    value = self.edits[editName].toPlainText()
                else:
                    value = self.edits[editName].text()

                self.headerData[editName] = value


        #
        # commit table data to server list
        #
        def commitServerData(self, changedItem:QTableWidgetItem) -> None:
            serverItem = self.serverList[changedItem.row()]
            colIndex = changedItem.column()
            newValue = changedItem.data(QtCore.Qt.EditRole)
            dataKey = ""

            if colIndex == 0:
                dataKey = "URL"
            elif colIndex == 1:
                dataKey = "DESCRIPTION"
            
            serverItem[dataKey] = newValue


        #
        # commit table data to tag list
        #
        def commitTagData(self, changedItem:QTableWidgetItem) -> None:
            tagItem = self.tagList[changedItem.row()]
            colIndex = changedItem.column()
            newValue = changedItem.data(QtCore.Qt.EditRole)
            dataKey = ""

            if colIndex == 0:
                dataKey = "NAME"
            elif colIndex == 1:
                dataKey = "DESCRIPTION"
            
            tagItem[dataKey] = newValue


        #
        # implemented
        # set data
        #
        def setData(self, data) -> None:
            self.headerData = data
            self.searchServerList(data)
            self.searchTagList(data)

            # set data to each edit
            for editName in self.edits:
                self.edits[editName].setText(data[editName])


        #
        # implemented
        # save data
        #
        def getData(self) -> Dict:
            self.commitHeaderData()

            return {
                "headerData": self.headerData,
                "serverList": self.serverList,
                "tagList": self.tagList
            }

        
        #
        # implemented
        # clear data
        #
        def clear(self) -> None:
            # clear header
            if DataUtil.isNotEmpty(self.headerData):
                self.headerData.clear()

            for editName in self.edits:
                self.edits[editName].setText("")

            # clear servers
            if DataUtil.isNotEmpty(self.serverList):
                self.serverList.clear()

            # clear tags
            if DataUtil.isNotEmpty(self.tagList):
                self.tagList.clear()

            self.tbl_serverList.clearContents()
            self.tbl_serverList.setRowCount(0)
            self.tbl_tagList.clearContents()
            self.tbl_tagList.setRowCount(0)



    #
    # tab2 - Path list
    #
    class OASPathsWidget(AbstactOASTabChildWidget, uic.loadUiType(OASConfig.getInstance().getConfig("ui_paths_path"))[0]):
        def __init__(self, mainWindow:OASMainWindow) -> None:
            super().__init__()

            self.__mainWindow = mainWindow

            # initialize data
            self.pathList = None
            self.pathHeaderListMap = {}
            self.pathResponseListMap = {}

            self.fireItemSelectionChangedEvent = True

            # initialize UI components
            self.setupUi(self)
            self.initUI()
            

        #
        # initialize GUI components
        #
        def initUI(self) -> None:
            # path table
            self.tbl_pathList.setHorizontalHeaderLabels(
                [ "Path", "HTTP Method", "Tag", "Operation ID", "Summary", "Request Body Content Type", "Request Body Schema", "Description" ]
            )
            self.tbl_pathList.itemSelectionChanged.connect(self.tblPathList_itemSelectionChangedHandler)
            self.tbl_pathList.itemChanged.connect(self.tblPathList_itemChanged)
            self.tbl_pathList.keyReleaseEvent = self.tblPathList_keyReleaseEvent

            # path header table
            self.tbl_pathHeaderList.setHorizontalHeaderLabels(
                [ "Name", "Type", "Required", "Description" ]
            )
            self.tbl_pathHeaderList.itemChanged.connect(self.tblPathHeaderList_itemChanged)
            self.tbl_pathHeaderList.keyReleaseEvent = self.tblPathHeaderList_keyReleaseEvent

            # path response table
            self.tbl_pathResponseList.setHorizontalHeaderLabels(
                [ "Status Code", "Content Type", "Schema", "Description" ]
            )
            self.tbl_pathResponseList.itemChanged.connect(self.tblPathResponseList_itemChanged)
            self.tbl_pathResponseList.keyReleaseEvent = self.tblPathResponseList_keyReleaseEvent

            # add/remove button for path
            self.btn_addNewPath.clicked.connect(self.btnAddNewPath_clickedHandler)
            self.btn_removePath.clicked.connect(self.btnRemovePath_clickedHandler)

            # add/remove button for header
            self.btn_addNewPathHeader.clicked.connect(self.btnAddNewPathHeader_clickedHandler)
            self.btn_removePathHeader.clicked.connect(self.btnRemovePathHeader_clickedHandler)

            # add/remove button for response
            self.btn_addNewPathResponse.clicked.connect(self.btnAddNewPathResponse_clickedHandler)
            self.btn_removePathResponse.clicked.connect(self.btnRemovePathResponse_clickedHandler)


        #
        # keyReleaseEvent handler for path table
        #
        def tblPathList_keyReleaseEvent(self, event:QKeyEvent) -> None:
            if event.key() == QtCore.Qt.Key_Insert:
                self.btnAddNewPath_clickedHandler()


        #
        # keyReleaseEvent handler for header table
        #
        def tblPathHeaderList_keyReleaseEvent(self, event:QKeyEvent) -> None:
            if event.key() == QtCore.Qt.Key_Insert:
                self.btnAddNewPathHeader_clickedHandler()


        #
        # keyReleaseEvent handler for response table
        #
        def tblPathResponseList_keyReleaseEvent(self, event:QKeyEvent) -> None:
            if event.key() == QtCore.Qt.Key_Insert:
                self.btnAddNewPathResponse_clickedHandler()


        #
        # itemSelectionChanged handler for path table
        #
        def tblPathList_itemSelectionChangedHandler(self) -> None:
            if self.fireItemSelectionChangedEvent and DataUtil.isNotEmpty(self.pathList):
                pathSeqKey = self.getCurrentPathSeqKey()

                self.updatePathHeaderData(pathSeqKey)
                self.updatePathResponseData(pathSeqKey)


        #
        # itemChanged handler for path table
        #
        def tblPathList_itemChanged(self, changedItem:QTableWidgetItem) -> None:
            self.commitPathData(changedItem)
            self.updatePathTableToContents()


        #
        # itemChanged handler for header table
        #
        def tblPathHeaderList_itemChanged(self, changedItem:QTableWidgetItem) -> None:
            self.commitPathHeaderData(changedItem)
            self.updatePathHeaderTableToContents()


        #
        # itemChanged handler for response table
        #
        def tblPathResponseList_itemChanged(self, changedItem:QTableWidgetItem) -> None:
            self.commitPathResponseData(changedItem)
            self.updatePathResponseTableToContents()


        #
        # clicked handler for add new path button
        #
        def btnAddNewPath_clickedHandler(self) -> None:
            if DataUtil.isEmpty(self.headerData):
                QMessageBox.warning(self, "", "Select the OAS header!")
                self.__mainWindow.selectTab(0)
                return

            if DataUtil.isEmpty(self.pathList):
                self.pathList = []

            # add new path row
            newMaxPathSeq = DataUtil.nvl(ListUtil.getMax(self.pathList, "PATH_SEQ"), 1)
            newPathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(newMaxPathSeq)

            newPath = {
                "UID": self.headerData["UID"],
                "PATH_SEQ": newMaxPathSeq,
                "PATH": "",
                "METHOD": "",
                "TAG_SEQ": "",
                "OPERATION_ID": "",
                "SUMMARY": "",
                "DESCRIPTION": "",
                "REQUEST_BODY_CONTENT_TYPE": "",
                "REQUEST_BODY_SCHEMA_SEQ": ""
            }
            self.pathList.append(newPath)
            self.pathResponseListMap[newPathSeqKey] = []
            

            # update path data
            self.updatePathData()

            # select row and start to edit first cell
            lastRowIndex = len(self.pathList) - 1

            self.tbl_pathList.selectRow(lastRowIndex)
            self.tbl_pathList.editItem(self.tbl_pathList.item(lastRowIndex, 0))

            # update response data        
            self.updatePathResponseData(newPathSeqKey)


        #
        # clicked handler for remove path button
        #
        def btnRemovePath_clickedHandler(self) -> None:
            currentRow = self.tbl_pathList.currentRow()
            
            if currentRow < 0:
                return

            pathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(self.pathList[currentRow]["PATH_SEQ"])

            # remove schema
            self.pathList.pop(currentRow)
            self.updatePathData()
            self.tbl_pathList.selectRow(len(self.pathList) - 1)

            # remove response list
            if DictUtil.isNotEmpty(self.pathResponseListMap, pathSeqKey):
                self.pathResponseListMap[pathSeqKey].clear()

            # property list
            currentRow = self.tbl_pathList.currentRow()

            if currentRow > -1:
                pathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(self.pathList[currentRow]["PATH_SEQ"])
                self.updatePathResponseData(pathSeqKey)
            else:
                self.tbl_pathList.setRowCount(0)


        #
        # clicked handler for add new header button
        #
        def btnAddNewPathHeader_clickedHandler(self) -> None:
            currentPathRow = self.tbl_pathList.currentRow()

            if currentPathRow < 0:
                QMessageBox.warning(self, "", "Select the path!")
                return

            pathData = self.pathList[currentPathRow]
            pathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(pathData["PATH_SEQ"])

            # add new header row
            if DictUtil.isEmpty(self.pathHeaderListMap, pathSeqKey):
                self.pathHeaderListMap[pathSeqKey] = []
                
            newHeader = {
                "UID": pathData["UID"],
                "PATH_SEQ": pathData["PATH_SEQ"],
                "HEADER_SEQ": -1,
                "NAME": "",
                "TYPE": "",
                "REQUIRED": "",
                "DESCRIPTION": ""
            }
            self.pathHeaderListMap[pathSeqKey].append(newHeader)

            # update header data
            self.updatePathHeaderData(pathSeqKey)

            # select row and start to edit first cell
            lastRowIndex = len(self.pathHeaderListMap[pathSeqKey]) - 1

            self.tbl_pathHeaderList.selectRow(lastRowIndex)
            self.tbl_pathHeaderList.editItem(self.tbl_pathHeaderList.item(lastRowIndex, 0))


        #
        # clicked handler for remove header button
        #
        def btnRemovePathHeader_clickedHandler(self) -> None:
            currentRow = self.tbl_pathHeaderList.currentRow()

            if currentRow < 0:
                return

            pathSeqKey = self.getCurrentPathSeqKey()

            # remove header
            self.pathHeaderListMap[pathSeqKey].pop(currentRow)

            self.updatePathHeaderData(pathSeqKey)
            self.tbl_pathHeaderList.selectRow(len( self.pathHeaderListMap[pathSeqKey]) - 1)


        #
        # clicked handler for add new response button
        #
        def btnAddNewPathResponse_clickedHandler(self) -> None:
            currentPathRow = self.tbl_pathList.currentRow()

            if currentPathRow < 0:
                QMessageBox.warning(self, "", "Select the path!")
                return

            pathData = self.pathList[currentPathRow]
            pathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(pathData["PATH_SEQ"])

            # add new property row
            if DictUtil.isEmpty( self.pathResponseListMap, pathSeqKey):
                self.pathResponseListMap[pathSeqKey] = []
                
            newResponse = {
                "UID": pathData["UID"],
                "PATH_SEQ": pathData["PATH_SEQ"],
                "STATUS_CD": "000",
                "CONTENT_TYPE": "",
                "DESCRIPTION": "",
                "SCHEMA_SEQ": ""
            }
            self.pathResponseListMap[pathSeqKey].append(newResponse)

            # update resopnse data
            self.updatePathResponseData(pathSeqKey)


            # select row and start to edit first cell
            lastRowIndex = len(self.pathResponseListMap[pathSeqKey]) - 1

            self.tbl_pathResponseList.selectRow(lastRowIndex)
            self.tbl_pathResponseList.editItem(self.tbl_pathResponseList.item(lastRowIndex, 0))


        #
        # clicked handler for remove response button
        #
        def btnRemovePathResponse_clickedHandler(self) -> None:
            currentRow = self.tbl_pathResponseList.currentRow()

            if currentRow < 0:
                return

            pathSeqKey = self.getCurrentPathSeqKey()

            # remove response
            self.pathResponseListMap[pathSeqKey].pop(currentRow)

            self.updatePathResponseData(pathSeqKey)
            self.tbl_pathResponseList.selectRow(len( self.pathResponseListMap[pathSeqKey]) - 1)


        #
        # currentTextChanged handler for methodCombo of the path table
        #
        def pathMethodCombo_currentTextChangedHandler(self, text:str) -> None:
            currentRow = self.tbl_pathList.currentRow()
            self.pathList[currentRow]["METHOD"] = text


        #
        # currentTextChanged handler for typeCombo of the header
        #
        def pathHeaderTypeCombo_currentTextChangedHandler(self, text:str) -> None:
            pathSeqKey = self.getCurrentPathSeqKey()
            currentRow = self.tbl_pathHeaderList.currentRow()

            self.pathHeaderListMap[pathSeqKey][currentRow]["TYPE"] = text


        #
        # currentTextChanged handler for requiredCombo of the header
        #
        def pathHeaderRequiredCombo_currentTextChangedHandler(self, text:str) -> None:
            currentPathRow = self.tbl_pathList.currentRow()
            pathSeqKey = self.getCurrentPathSeqKey()

            currentRow = self.tbl_pathHeaderList.currentRow()
            
            self.pathHeaderListMap[pathSeqKey][currentRow]["REQUIRED"] = text


        #
        # return current path seq for key
        #
        def getCurrentPathSeqKey(self) -> str:
            currentRow = self.tbl_pathList.currentRow()
            return OASConstants.PATH_SEQ_KEY_PREFIX + str(self.pathList[currentRow]["PATH_SEQ"])


        #
        # update path table to it's contents
        #
        def updatePathTableToContents(self) -> None:
            self.tbl_pathList.resizeColumnsToContents()
            self.tbl_pathList.resizeRowsToContents()


        #
        # update header table to it's contents
        #
        def updatePathHeaderTableToContents(self) -> None:
            self.tbl_pathHeaderList.resizeColumnsToContents()
            self.tbl_pathHeaderList.resizeRowsToContents()


        #
        # update response table to it's contents
        #
        def updatePathResponseTableToContents(self) -> None:
            self.tbl_pathResponseList.resizeColumnsToContents()
            self.tbl_pathResponseList.resizeRowsToContents()


        #
        # search path list
        #
        def searchPathList(self, param) -> None:
            #
            # 1. clear previous lists
            if DataUtil.isNotEmpty(self.pathList):
                self.pathList.clear()

            if DataUtil.isNotEmpty(self.pathHeaderListMap):
                self.pathHeaderListMap.clear()

            if DataUtil.isNotEmpty(self.pathResponseListMap):
                self.pathResponseListMap.clear()

            self.fireItemSelectionChangedEvent = False
            self.tbl_pathList.clearContents()
            self.tbl_pathList.setRowCount(0)
            self.tbl_pathResponseList.clearContents()
            self.tbl_pathResponseList.setRowCount(0)
            self.fireItemSelectionChangedEvent = True

            #
            # 2. get path list
            self.pathList = self.oasDataService.getPathList(parameter=param)

            #
            # 3. bind list to table
            self.updatePathData()

            #
            # 4. get header list
            param["PATH_SEQ"] = ""
            pathHeaderList = self.oasDataService.getPathHeaderList(parameter=param)

            for header in pathHeaderList:
                pathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(header["PATH_SEQ"])

                if DictUtil.isEmpty(self.pathHeaderListMap, pathSeqKey):
                    self.pathHeaderListMap[pathSeqKey] = []

                self.pathHeaderListMap[pathSeqKey].append(header)

            #
            # 5. get response list
            pathResponseList = self.oasDataService.getPathResponseList(parameter=param)

            for header in pathResponseList:
                pathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(header["PATH_SEQ"])

                if DictUtil.isEmpty(self.pathResponseListMap, pathSeqKey):
                    self.pathResponseListMap[pathSeqKey] = []

                self.pathResponseListMap[pathSeqKey].append(header)

            #
            # 5. select the first row
            if len(self.pathList) > 0:
                self.tbl_pathList.selectRow(0)


        #
        # bind current data to path table
        #
        def updatePathData(self) -> None:
            rowCount = len(self.pathList)
            
            self.tbl_pathList.setRowCount(rowCount)

            for index in range(rowCount):
                methodCombo = QWidgetUtil.createComboBox(
                    ["post", "get", "put"], initValue=self.pathList[index]["METHOD"], currentTextChangedHandler=self.pathMethodCombo_currentTextChangedHandler
                )

                self.tbl_pathList.setItem(index, 0, QTableWidgetItem(self.pathList[index]["PATH"]))
                self.tbl_pathList.setItem(index, 1, QTableWidgetItem(self.pathList[index]["METHOD"]))
                self.tbl_pathList.setCellWidget(index, 1, methodCombo)
                self.tbl_pathList.setItem(index, 2, QTableWidgetItem(self.pathList[index]["TAG_SEQ"]))
                self.tbl_pathList.setItem(index, 3, QTableWidgetItem(self.pathList[index]["OPERATION_ID"]))
                self.tbl_pathList.setItem(index, 4, QTableWidgetItem(self.pathList[index]["SUMMARY"]))
                self.tbl_pathList.setItem(index, 5, QTableWidgetItem(self.pathList[index]["REQUEST_BODY_CONTENT_TYPE"]))
                self.tbl_pathList.setItem(index, 6, QTableWidgetItem(self.pathList[index]["REQUEST_BODY_SCHEMA_SEQ"]))
                self.tbl_pathList.setItem(index, 7, QTableWidgetItem(self.pathList[index]["DESCRIPTION"]))

            self.updatePathTableToContents()

        
        #
        # bind current data to header table
        #
        def updatePathHeaderData(self, pathSeqKey:str) -> None:
            if DictUtil.isEmpty(self.pathHeaderListMap, pathSeqKey):
                self.tbl_pathHeaderList.clearContents()
                self.tbl_pathHeaderList.setRowCount(0)

            else:
                pathHeaderList = self.pathHeaderListMap[pathSeqKey]
                
                rowCount = len(pathHeaderList)
                self.tbl_pathHeaderList.setRowCount(rowCount)

                for index in range(rowCount):
                    typeCombo = QWidgetUtil.createComboBox(
                        ["string", "integer", "number", "array", "boolean", "object"],
                        initValue=pathHeaderList[index]["TYPE"],
                        currentTextChangedHandler=self.pathHeaderTypeCombo_currentTextChangedHandler
                    )

                    requiredCombo = QWidgetUtil.createComboBox(["Y", "N"], currentTextChangedHandler=self.pathHeaderRequiredCombo_currentTextChangedHandler)
                    requiredCombo.setCurrentText(pathHeaderList[index]["REQUIRED"])

                    self.tbl_pathHeaderList.setItem(index, 0, QTableWidgetItem(str(pathHeaderList[index]["NAME"])))
                    self.tbl_pathHeaderList.setItem(index, 1, QTableWidgetItem(pathHeaderList[index]["TYPE"]))
                    self.tbl_pathHeaderList.setCellWidget(index, 1, typeCombo)
                    self.tbl_pathHeaderList.setItem(index, 2, QTableWidgetItem(pathHeaderList[index]["REQUIRED"]))
                    self.tbl_pathHeaderList.setCellWidget(index, 2, requiredCombo)
                    self.tbl_pathHeaderList.setItem(index, 3, QTableWidgetItem(pathHeaderList[index]["DESCRIPTION"]))

                self.updatePathHeaderTableToContents()


        #
        # bind current data to response table
        #
        def updatePathResponseData(self, pathSeqKey:str) -> None:
            if DictUtil.isEmpty(self.pathResponseListMap, pathSeqKey):
                self.tbl_pathResponseList.clearContents()
                self.tbl_pathResponseList.setRowCount(0)

            else:
                responseList = self.pathResponseListMap[pathSeqKey]
                
                rowCount = len(responseList)
                self.tbl_pathResponseList.setRowCount(rowCount)

                for index in range(rowCount):
                    self.tbl_pathResponseList.setItem(index, 0, QTableWidgetItem(str(responseList[index]["STATUS_CD"])))
                    self.tbl_pathResponseList.setItem(index, 1, QTableWidgetItem(responseList[index]["CONTENT_TYPE"]))
                    self.tbl_pathResponseList.setItem(index, 2, QTableWidgetItem(responseList[index]["SCHEMA_SEQ"]))
                    self.tbl_pathResponseList.setItem(index, 3, QTableWidgetItem(responseList[index]["DESCRIPTION"]))

                self.updatePathResponseTableToContents()


        #
        # commit table data to path list
        #
        def commitPathData(self, changedItem:QTableWidgetItem) -> None:
            pathItem = self.pathList[changedItem.row()]
            colIndex = changedItem.column()
            newValue = changedItem.data(QtCore.Qt.EditRole)
            dataKey = ""

            if colIndex == 0:
                dataKey = "PATH"
            elif colIndex == 1:
                dataKey = "METHOD"
            elif colIndex == 1:
                dataKey = "TAG_SEQ"
            elif colIndex == 1:
                dataKey = "OPERATION_ID"
            elif colIndex == 1:
                dataKey = "SUMMARY"
            elif colIndex == 1:
                dataKey = "REQUEST_BODY_CONTENT_TYPE"
            elif colIndex == 1:
                dataKey = "REQUEST_BODY_SCHEMA_SEQ"
            elif colIndex == 1:
                dataKey = "DESCRIPTION"
            
            pathItem[dataKey] = newValue


        #
        # commit table data to header list
        #
        def commitPathHeaderData(self, changedItem:QTableWidgetItem) -> None:
            currentPathRow = self.tbl_pathList.currentRow()
            pathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(self.pathList[currentPathRow]["PATH_SEQ"])
            headerItem = self.pathHeaderListMap[pathSeqKey][changedItem.row()]

            colIndex = changedItem.column()
            newValue = changedItem.data(QtCore.Qt.EditRole)
            dataKey = ""

            if colIndex == 0:
                dataKey = "NAME"
            elif colIndex == 1:
                dataKey = "TYPE"
            elif colIndex == 2:
                dataKey = "REQUIRED"
            elif colIndex == 3:
                dataKey = "DESCRIPTION"

            headerItem[dataKey] = newValue


        #
        # commit table data to response list
        #
        def commitPathResponseData(self, changedItem:QTableWidgetItem) -> None:
            currentPathRow = self.tbl_pathList.currentRow()
            pathSeqKey = OASConstants.PATH_SEQ_KEY_PREFIX + str(self.pathList[currentPathRow]["PATH_SEQ"])
            responseItem = self.pathResponseListMap[pathSeqKey][changedItem.row()]

            colIndex = changedItem.column()
            newValue = changedItem.data(QtCore.Qt.EditRole)
            dataKey = ""

            if colIndex == 0:
                dataKey = "STATUS_CD"            
            elif colIndex == 1:
                dataKey = "CONTENT_TYPE"
            elif colIndex == 2:
                dataKey = "SCHEMA_SEQ"
            elif colIndex == 3:
                dataKey = "DESCRIPTION"

            responseItem[dataKey] = newValue


        #
        # implemented
        # set new data
        #
        def setData(self, data) -> None:
            self.headerData = data
            self.searchPathList(data)


        #
        # implemented
        # save data
        #
        def getData(self) -> Dict:
            return {
                "pathList": self.pathList,
                "pathHeaderListMap": self.pathHeaderListMap,
                "pathResponseListMap": self.pathResponseListMap
            }


        #
        # implemented
        # clear data
        #
        def clear(self) -> None:
            # clear paths
            if DataUtil.isNotEmpty(self.pathList):
                self.pathList.clear()

            self.tbl_pathList.clearContents()
            self.tbl_pathList.setRowCount(0)

            # clear responses
            if DataUtil.isNotEmpty(self.pathResponseListMap):
                self.pathResponseListMap.clear()

            self.tbl_pathResponseList.clearContents()
            self.tbl_pathResponseList.setRowCount(0)



    #
    # tab3 - Schemas and their properties
    #
    class OASSchemasWidget(AbstactOASTabChildWidget, uic.loadUiType(OASConfig.getInstance().getConfig("ui_schemas_path"))[0]):

        #
        # Constructor
        #
        def __init__(self, mainWindow:OASMainWindow) -> None:
            super().__init__()

            self.__mainWindow = mainWindow

            # initialize data
            self.headerData = None
            self.schemaList = None
            self.schemaProperyListMap = {}

            self.fireItemSelectionChangedEvent = True

            # initialize UI components
            self.setupUi(self)
            self.initUI()
            

        #
        # initialize UI components  
        #
        def initUI(self) -> None:
            # schema table
            self.tbl_schemaList.setHorizontalHeaderLabels([ "Name", "Type" ])
            self.tbl_schemaList.itemSelectionChanged.connect(self.tblSchemaList_itemSelectionChangedHandler)
            self.tbl_schemaList.itemChanged.connect(self.tblSchemaList_itemChanged)
            self.tbl_schemaList.keyReleaseEvent = self.tblSchemaList_keyReleaseEvent
            self.tbl_schemaList.setSelectionMode(QAbstractItemView.SingleSelection)

            # schema property table
            self.tbl_schemaPropList.setHorizontalHeaderLabels([ "Name", "Type", "Required", "Value", "Ref Schema", "Description" ])
            self.tbl_schemaPropList.itemChanged.connect(self.tblSchemaPropList_itemChanged)
            self.tbl_schemaPropList.keyReleaseEvent = self.tblSchemaPropList_keyReleaseEvent
            self.tbl_schemaPropList.setSelectionMode(QAbstractItemView.SingleSelection)

            # add/remove button for schema
            self.btn_addNewSchema.clicked.connect(self.btnAddNewSchema_clickedHandler)
            self.btn_removeSchema.clicked.connect(self.btnRemoveSchema_clickedHandler)

            # add/remove button for schema property
            self.btn_addNewProp.clicked.connect(self.btnAddNewSchemaProp_clickedHandler)
            self.btn_removeProp.clicked.connect(self.btnRemoveProp_clickedHandler)


        #
        # keyReleaseEvent handler for schema table
        #
        def tblSchemaList_keyReleaseEvent(self, event:QKeyEvent) -> None:
            if event.key() == QtCore.Qt.Key_Insert:
                self.btnAddNewSchema_clickedHandler()


        #
        # keyReleaseEvent handler for property table
        #
        def tblSchemaPropList_keyReleaseEvent(self, event:QKeyEvent) -> None:
            if event.key() == QtCore.Qt.Key_Insert:
                self.btnAddNewSchemaProp_clickedHandler()


        #
        # itemSelectionChanged handler for schema table
        #
        def tblSchemaList_itemSelectionChangedHandler(self) -> None:
            if self.fireItemSelectionChangedEvent and DataUtil.isNotEmpty(self.schemaList):
                schemaSeqKey = self.getCurrentSchemaSeqKey()

                self.updateSchemaPropData(schemaSeqKey)


        #
        # cellChanged handler for schema table
        #
        def tblSchemaList_itemChanged(self, changedItem:QTableWidgetItem) -> None:
            self.commitSchemaData(changedItem)
            self.updateSchemaTableToContents()


        #
        # cellChanged handler for schema property table
        #
        def tblSchemaPropList_itemChanged(self, changedItem:QTableWidgetItem) -> None:
            self.commitSchemaPropData(changedItem)
            self.updateSchemaPropTableToContents()


        #
        # clicked handler for add new schema button
        #
        def btnAddNewSchema_clickedHandler(self) -> None:
            if DataUtil.isEmpty(self.headerData):
                QMessageBox.warning(self, "", "Select the OAS header!")
                self.__mainWindow.selectTab(0)
                return

            if DataUtil.isEmpty(self.schemaList):
                self.schemaList = []

            # add new schema row
            newMaxSchemaSeq = ListUtil.getMax(self.schemaList, "SCHEMA_SEQ")
            newMaxSchemaSeq = 1 if newMaxSchemaSeq == None else int(newMaxSchemaSeq) + 1
            newSchemaSeqKey = OASConstants.SCHEMA_SEQ_KEY_PREFIX + str(newMaxSchemaSeq)

            newSchema = {
                "UID": self.headerData["UID"],
                "SCHEMA_SEQ": newMaxSchemaSeq,
                "NAME": "",
                "TYPE": "",
            }
            self.schemaList.append(newSchema)
            self.schemaProperyListMap[newSchemaSeqKey] = []
            

            # update schema data
            self.updateSchemaData()

            # select row and start to edit first cell
            lastRowIndex = len(self.schemaList) - 1

            self.tbl_schemaList.selectRow(lastRowIndex)
            self.tbl_schemaList.editItem(self.tbl_schemaList.item(lastRowIndex, 0))

            # update property data        
            self.updateSchemaPropData(newSchemaSeqKey)


        #
        # clicked handler for remove schema button
        #
        def btnRemoveSchema_clickedHandler(self) -> None:
            currentRow = self.tbl_schemaList.currentRow()
            
            if currentRow < 0:
                return

            schemaSeqKey = OASConstants.SCHEMA_SEQ_KEY_PREFIX + str(self.schemaList[currentRow]["SCHEMA_SEQ"])

            # remove schema
            self.schemaList.pop(currentRow)
            self.updateSchemaData()
            self.tbl_schemaList.selectRow(len(self.schemaList) - 1)

            # remove schema property list
            if DictUtil.isNotEmpty(self.schemaProperyListMap, schemaSeqKey):
                self.schemaProperyListMap[schemaSeqKey].clear()

            # property list
            currentRow = self.tbl_schemaList.currentRow()

            if currentRow > -1:
                schemaSeqKey = OASConstants.SCHEMA_SEQ_KEY_PREFIX + str(self.schemaList[currentRow]["SCHEMA_SEQ"])
                self.updateSchemaPropData(schemaSeqKey)
            else:
                self.tbl_schemaPropList.setRowCount(0)


        #
        # clicked handler for add new property button
        #
        def btnAddNewSchemaProp_clickedHandler(self) -> None:
            currentSchemaRow = self.tbl_schemaList.currentRow()

            if currentSchemaRow < 0:
                QMessageBox.warning(self, "", "Select the schema!")
                return

            schemaData = self.schemaList[currentSchemaRow]
            schemaSeqKey = OASConstants.SCHEMA_SEQ_KEY_PREFIX + str(schemaData["SCHEMA_SEQ"])

            # add new property row
            if DictUtil.isEmpty(self.schemaProperyListMap, schemaSeqKey):
                self.schemaProperyListMap[schemaSeqKey] = []
                
            #newMaxPropSeq = ListUtil.getMax(self.properyListMap[schemaSeqKey], "PROP_SEQ")
            #newMaxPropSeq = 1 if newMaxPropSeq == None else int(newMaxPropSeq) + 1
            newMaxPropSeq = -1

            newSchemaProp = {
                "UID": schemaData["UID"],
                "SCHEMA_SEQ": schemaData["SCHEMA_SEQ"],
                "PROP_SEQ": newMaxPropSeq,
                "NAME": "",
                "TYPE": "",
                "REQUIRED": "",
                "VALUE": "",
                "REF_SCHEMA_SEQ": "",
                "MAX_LENGTH": 0,
                "DESCRIPTION": "",
                "REQUIRED": ""
            }
            self.schemaProperyListMap[schemaSeqKey].append(newSchemaProp)

            # update schema property data
            self.updateSchemaPropData(schemaSeqKey)

            # select row and start to edit first cell
            lastRowIndex = len(self.schemaProperyListMap[schemaSeqKey]) - 1

            self.tbl_schemaPropList.selectRow(lastRowIndex)
            self.tbl_schemaPropList.editItem(self.tbl_schemaPropList.item(lastRowIndex, 0))


        #
        # clicked handler for remove property button
        #
        def btnRemoveProp_clickedHandler(self) -> None:
            currentRow = self.tbl_schemaPropList.currentRow()

            if currentRow < 0:
                return

            schemaSeqKey = self.getCurrentSchemaSeqKey()

            # remove property
            self.schemaProperyListMap[schemaSeqKey].pop(currentRow)

            self.updateSchemaPropData(schemaSeqKey)
            self.tbl_schemaPropList.selectRow(len(self.schemaProperyListMap[schemaSeqKey]) - 1)


        #
        # currentTextChanged handler for typeCombo of the schema
        #
        def schemaTypeCombo_currentTextChangedHandler(self, text:str) -> None:
            currentRow = self.tbl_schemaList.currentRow()
            self.schemaList[currentRow]["TYPE"] = text


        #
        # currentTextChanged handler for typeCombo of the schema property
        #
        def schemaPropTypeCombo_currentTextChangedHandler(self, text:str) -> None:
            schemaSeqKey = self.getCurrentSchemaSeqKey()
            currentRow = self.tbl_schemaPropList.currentRow()

            self.schemaProperyListMap[schemaSeqKey][currentRow]["TYPE"] = text


        #
        # currentTextChanged handler for requiredCombo of the schema property
        #
        def schemaPropRequiredCombo_currentTextChangedHandler(self, text:str) -> None:
            schemaSeqKey = self.getCurrentSchemaSeqKey()
            currentRow = self.tbl_schemaPropList.currentRow()

            self.schemaProperyListMap[schemaSeqKey][currentRow]["REQUIRED"] = text


        #
        # return current schema seq for key
        #
        def getCurrentSchemaSeqKey(self) -> str:
            currentSchemaRow = self.tbl_schemaList.currentRow()
            return OASConstants.SCHEMA_SEQ_KEY_PREFIX + str(self.schemaList[currentSchemaRow]["SCHEMA_SEQ"])


        #
        # update schema table to it's contents
        #
        def updateSchemaTableToContents(self) -> None:
            self.tbl_schemaList.resizeColumnsToContents()
            self.tbl_schemaList.resizeRowsToContents()


        #
        # update property table to it's contents
        #
        def updateSchemaPropTableToContents(self) -> None:
            self.tbl_schemaPropList.resizeColumnsToContents()
            self.tbl_schemaPropList.resizeRowsToContents()


        #
        # search schema and property list
        #
        def searchSchemaList(self, param) -> None:
            #
            # 1. clear previous lists
            if DataUtil.isNotEmpty(self.schemaList):
                self.schemaList.clear()

            if DataUtil.isNotEmpty(self.schemaProperyListMap):
                self.schemaProperyListMap.clear()

            self.fireItemSelectionChangedEvent = False
            self.tbl_schemaList.clearContents()
            self.tbl_schemaList.setRowCount(0)
            self.tbl_schemaPropList.clearContents()
            self.tbl_schemaPropList.setRowCount(0)
            self.fireItemSelectionChangedEvent = True

            #
            # 2. get schema list
            self.schemaList = self.oasDataService.getSchemaList(parameter=param)

            #
            # 3. bind list to table
            self.updateSchemaData()

            #
            # 4. schema property list
            param["SCHEMA_SEQ"] = ""
            schemaPropList = self.oasDataService.getSchemaPropList(parameter=param)

            # classify schema property for each schema
            for schemaProp in schemaPropList:
                schemaSeqKey = OASConstants.SCHEMA_SEQ_KEY_PREFIX + str(schemaProp["SCHEMA_SEQ"])

                if DictUtil.isEmpty(self.schemaProperyListMap, schemaSeqKey):
                    self.schemaProperyListMap[schemaSeqKey] = []

                self.schemaProperyListMap[schemaSeqKey].append(schemaProp)

            #
            # 5. select the first row
            if len(self.schemaList) > 0:
                self.tbl_schemaList.selectRow(0)


        #
        # bind current data to table
        #
        def updateSchemaData(self) -> None:
            rowCount = len(self.schemaList)
            
            self.tbl_schemaList.setRowCount(rowCount)

            for index in range(rowCount):
                typeCombo = QWidgetUtil.createComboBox(
                    ["string", "integer", "number", "array", "boolean", "object"],
                    initValue=self.schemaList[index]["TYPE"],
                    currentTextChangedHandler=self.schemaTypeCombo_currentTextChangedHandler
                )
                self.tbl_schemaList.setItem(index, 0, QTableWidgetItem(self.schemaList[index]["NAME"]))
                self.tbl_schemaList.setItem(index, 1, QTableWidgetItem(self.schemaList[index]["TYPE"]))
                self.tbl_schemaList.setCellWidget(index, 1, typeCombo)

            self.updateSchemaTableToContents()


        #
        # update current data to property table
        #
        def updateSchemaPropData(self, schemaSeqKey) -> None:
            if DictUtil.isEmpty(self.schemaProperyListMap, schemaSeqKey):
                self.tbl_schemaPropList.clearContents()
                self.tbl_schemaPropList.setRowCount(0)
                
            else:
                schemaPropList = self.schemaProperyListMap[schemaSeqKey]
                
                rowCount = len(schemaPropList)
                self.tbl_schemaPropList.setRowCount(rowCount)

                for index in range(rowCount):
                    typeCombo = QWidgetUtil.createComboBox(
                        ["string", "integer", "number", "array", "boolean", "object"],
                        initValue=schemaPropList[index]["TYPE"],
                        currentTextChangedHandler=self.schemaPropTypeCombo_currentTextChangedHandler
                    )

                    requiredCombo = QWidgetUtil.createComboBox(
                        ["Y", "N"], currentTextChangedHandler=self.schemaPropRequiredCombo_currentTextChangedHandler
                    )
                    requiredCombo.setCurrentText(schemaPropList[index]["REQUIRED"])

                    self.tbl_schemaPropList.setItem(index, 0, QTableWidgetItem(schemaPropList[index]["NAME"]))
                    self.tbl_schemaPropList.setItem(index, 1, QTableWidgetItem(schemaPropList[index]["TYPE"]))
                    self.tbl_schemaPropList.setCellWidget(index, 1, typeCombo)
                    self.tbl_schemaPropList.setItem(index, 2, QTableWidgetItem(schemaPropList[index]["REQUIRED"]))
                    self.tbl_schemaPropList.setCellWidget(index, 2, requiredCombo)
                    self.tbl_schemaPropList.setItem(index, 3, QTableWidgetItem(schemaPropList[index]["VALUE"]))
                    self.tbl_schemaPropList.setItem(index, 4, QTableWidgetItem(schemaPropList[index]["REF_SCHEMA_SEQ"]))
                    self.tbl_schemaPropList.setItem(index, 5, QTableWidgetItem(schemaPropList[index]["DESCRIPTION"]))

                self.updateSchemaPropTableToContents()


        #
        # commit table data to schema list
        #
        def commitSchemaData(self, changedItem:QTableWidgetItem) -> None:
            schemaItem = self.schemaList[changedItem.row()]
            colIndex = changedItem.column()
            newValue = changedItem.data(QtCore.Qt.EditRole)
            dataKey = ""

            if colIndex == 0:
                dataKey = "NAME"
            elif colIndex == 1:
                dataKey = "TYPE"
            
            schemaItem[dataKey] = newValue


        #
        # commit table data to list
        #
        def commitSchemaPropData(self, changedItem:QTableWidgetItem) -> None:
            # currentSchemaRow = self.tbl_schemaList.currentRow()
            # schemaSeqKey = OASConstants.SCHEMA_SEQ_KEY_PREFIX + str(self.schemaList[currentSchemaRow]["SCHEMA_SEQ"])
            schemaSeqKey = self.getCurrentSchemaSeqKey()
            propItem = self.schemaProperyListMap[schemaSeqKey][changedItem.row()]

            colIndex = changedItem.column()
            newValue = changedItem.data(QtCore.Qt.EditRole)
            dataKey = ""
            
            if colIndex == 0:
                dataKey = "NAME"
            elif colIndex == 1:
                dataKey = "TYPE"
            elif colIndex == 2:
                dataKey = "REQUIRED"
            elif colIndex == 3:
                dataKey = "VALUE"
            elif colIndex == 4:
                dataKey = "REF_SCHEMA_SEQ"
            elif colIndex == 5:
                dataKey = "DESCRIPTION"

            propItem[dataKey] = newValue


        #
        # set new data
        #
        def setData(self, data) -> None:
            self.headerData = data
            self.searchSchemaList(data)


        #
        # save data
        #
        def getData(self) -> Dict:
            return {
                "schemaList": self.schemaList,
                "propertyListMap": self.schemaProperyListMap
            }


        #
        # implemented
        # clear data
        #
        def clear(self) -> None:
            # clear schemas
            if DataUtil.isNotEmpty(self.schemaList):
                self.schemaList.clear()

            self.tbl_schemaList.clearContents()
            self.tbl_schemaList.setRowCount(0)

            # clear properties
            if DataUtil.isNotEmpty(self.schemaProperyListMap):
                self.schemaProperyListMap.clear()

            self.tbl_schemaPropList.clearContents()
            self.tbl_schemaPropList.setRowCount(0)
             


if __name__ == "__main__":
    thisApp = QApplication(sys.argv)

    oasDataService = OASSQLite3DataService.getInstance()
    oasMainWindow = OASMainWindow(oasDataService)

    qtmodern.styles.dark(thisApp)
    
    modernWindow = qtmodern.windows.ModernWindow(oasMainWindow)
    modernWindow.show()

    # oasMainWindow.show()
    thisApp.exec_()
