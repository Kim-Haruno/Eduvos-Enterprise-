class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.appName = "Eduvos Enterprise Application"
            cls._instance.version = "1.0"
            cls._instance.environment = "Development"

        return cls._instance

    def displayConfig(self):
        print("Application Name:", self.appName)
        print("Version:", self.version)
        print("Environment:", self.environment)