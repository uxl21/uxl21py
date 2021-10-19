"""
    Copyright (c) 2021 uxl21 <uxl21x@gmail.com>
    This file is a part of uxl21py

    
    Author
    -------
    uxl21
"""

class Data:
    """
        Data class containing data classes related to REST API.

        Author
        -------
        uxl21
    """

    class Controller:
        """
            Data class representing the Controller for REST API.

            Author
            -------
            uxl21
        """

        def __init__(self) -> None:
            self.process = None
            self.basePackage = None
            self.className = None
            self.tag = None
            self.tagDescription = None
            self.path = None
            self.endpoints = [] # array of Endpoint


    class Endpoint:
        """
            Data class representing the endpoint of Controller for REST API.

            Author
            -------
            uxl21
        """

        def __init__(self) -> None:
            self.name = None
            self.httpMethods = []
            self.path = None
            self.pathVars = []
            self.parameters = []
            self.parameterType = None   # json, form
            self.returnType = None
            self.responseType = None  # json, xml, string
            self.summary = None
            self.responses = [] # array of APIResponse


    class APIResponse:
        """
            Data class representing the API response of endpoint for REST API.

            Author
            -------
            uxl21
        """

        def __init__(self, responseCode, description, mediaType, encoding) -> None:
            self.responseCode = responseCode
            self.description = description
            self.mediaType = mediaType
            self.encoding = encoding


    class Parameter:
        """
            Data class representing the parameter of endpoint for REST API.

            Author
            -------
            uxl21
        """

        def __init__(self, type, name) -> None:
            self.type = type
            self.name = name





class RESTAPIConstants:
    # for controller class
    CONTROLLER_CLASS_TEMPLATE  = '''
        package {basePackage}.controller;

        import java.util.*;

        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.web.bind.annotation.PathVariable;
        import org.springframework.web.bind.annotation.RequestMapping;
        import org.springframework.web.bind.annotation.RequestMethod;
        import org.springframework.web.bind.annotation.ResponseBody;
        import org.springframework.web.bind.annotation.RestController;

        import io.swagger.v3.oas.annotations.Operation;
        import io.swagger.v3.oas.annotations.Parameter;
        import io.swagger.v3.oas.annotations.media.Content;
        import io.swagger.v3.oas.annotations.media.Encoding;
        import io.swagger.v3.oas.annotations.responses.ApiResponse;
        import io.swagger.v3.oas.annotations.responses.ApiResponses;
        import io.swagger.v3.oas.annotations.tags.Tag;

        import net.uxl21.uxl21j.base.BaseController;

        import {basePackage}.service.{process}Service;


        @Tag(name = "{tag}", description = "{tagDescription}")
        @RestController
        @RequestMapping(path = "{path}")
        public class {className} extends BaseController {startBracket}

            @Autowired
            private {process}Service {processLower}Service = null;

            {methods}
        
        {endBracket}
    '''

    ENDPOINT_TEMPLATE = '''
            @Operation(summary = "{summary}")
            @RequestMapping(path = "{path}", method = {startBracket}{httpMethod}{endBracket})
            @ApiResponses(
                value = {startBracket}
                    {apiResponses}
                {endBracket}
            )
            @ResponseBody
            public {returnType} {name}({pathVars}{parameters}) {startBracket}
                return null;
            {endBracket}
    '''

    API_RESPONSE_TEMPLATE = '''@ApiResponse(responseCode = "{responseCode}", description = "{description}", content = {startBracket}@Content(mediaType = "{mediaType}", encoding = @Encoding(name = "{encoding}")){endBracket})'''


    # for service class
    SERVICE_CLASS_TEMPLATE = '''
        package {basePackage}.service;

        import java.util.*;

        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.stereotype.Service;

        import net.uxl21.uxl21j.base.BaseService;
        import {basePackage}.dao.{process}DAO;


        @Service(value="{processLower}Service")
        public class {process}Service extends BaseService {startBracket}
            
            @Autowired
            private {process}DAO {processLower}DAO = null;

        {endBracket}
    '''

    # for DAO class
    DAO_CLASS_TEMPLATE = '''
        package {basePackage}.dao;

        import java.util.*;

        import org.springframework.stereotype.Repository;

        import net.uxl21.uxl21j.base.BaseDAO;


        @Repository(value="{processLower}DAO")
        public class {process}DAO extends BaseDAO {startBracket}
            
        {endBracket}
    '''




class RESTAPIGenerator:
    """
        REST API source code generator.

        Author
        -------
        uxl21
    """

    def generate(controller:Data.Controller) -> str:
        """
            Generates source code contents.

            Parameters
            -------
            controller: Data.Controller
                Data.Controller instance to generate source code contents.

            Author
            -------
            uxl21
        """

        for endpoint in controller.endpoints:
            # @RequestMapping - method
            count = len(endpoint.httpMethods)
            httpMethodStr = ""

            for i in range(0, count):
                httpMethodStr += "RequestMethod." + str(endpoint.httpMethods[i]).upper()

                if i < count - 1:
                    httpMethodStr += ", "
            

            # @ApiResponses
            count = len(endpoint.responses)
            apiResponsesSrc = ""

            for i in range(0, count):
                apiResponsesSrc += RESTAPIConstants.API_RESPONSE_TEMPLATE.format(
                    responseCode=endpoint.responses[i].responseCode, description=endpoint.responses[i].description,
                    mediaType=endpoint.responses[i].mediaType, encoding=endpoint.responses[i].encoding,
                    startBracket="{", endBracket="}"
                )

                if i < count - 1:
                    apiResponsesSrc += ",\n"


            # @PathVariable
            count = len(endpoint.pathVars)
            pathVarsSrc = ""

            for i in range(0, count):
                pathVarsSrc += ("@PathVariable final String " + endpoint.pathVars[i])

                if i < count - 1:
                    pathVarsSrc += ", "


            # parameters
            if count > 0:
                parametersSrc = ", "

            count = len(endpoint.parameters)        

            for i in range(0, count):
                parametersSrc += (endpoint.parameters[i].type + " " + endpoint.parameters[i].name)

                if i < count - 1:
                    parametersSrc += ", "


            # complte endpoint
            endpointSrc = ""
            endpointSrc += RESTAPIConstants.ENDPOINT_TEMPLATE.format(
                summary=endpoint.summary, 
                path=endpoint.path, httpMethod=httpMethodStr,
                apiResponses=apiResponsesSrc,
                returnType=endpoint.returnType, name=endpoint.name, pathVars=pathVarsSrc, parameters=parametersSrc,
                startBracket="{", endBracket="}"
            )

            
        classSrc = RESTAPIConstants.CONTROLLER_CLASS_TEMPLATE.format(
            basePackage=controller.basePackage, tag=controller.tag, tagDescription=controller.tagDescription,
            path=controller.path, className=controller.className, process=controller.process,
            processLower=controller.process.lower(), methods=endpointSrc,
            startBracket="{", endBracket="}"
        )

        return classSrc




if __name__ == "__main__":
    controller = Data.Controller()
    controller.basePackage = "net.uxl21.uxl21j.restapi.example"
    controller.tag = "Config"
    controller.process = "Config"
    controller.className = controller.process + "Controller"
    controller.tagDescription = "API for Configurations"
    controller.path = "${uxl21j.restapi.version}/config"

    configList = Data.Endpoint()
    configList.name = "searchConfigList"
    configList.httpMethods = [ "GET", "POST" ]
    configList.path = "/list/{siteCd}"
    configList.pathVars = [ "siteCd" ]
    configList.returnType = "List<Map<String, Object>>"
    configList.responseType = "json"
    configList.summary = "Get configuration list"
    configList.responses = [
        Data.APIResponse("200", "Configuration list", "application/json", "utf-8"),
        Data.APIResponse("400", "Invalid access or authorization token", "application/json", "utf-8")
    ]
    configList.parameters = [
        Data.Parameter("Map<String, Object>", "param")
    ]
    controller.endpoints = [ configList ]

    print(RESTAPIGenerator.generate(controller))