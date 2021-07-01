class Controller:

    def __init__(self) -> None:
        self.package = None
        self.className = None
        self.context = None
        self.endpoints = []




class Endpoint:

    def __init__(self) -> None:
        self.name = None
        self.httpMethod = None
        self.path = None
        self.pathVars = []
        self.parameters = []
        self.returnType = None


