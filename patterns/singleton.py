import threading
from typing import Any


class AppConfig:

    _instance: "AppConfig | None" = None
    _lock = threading.Lock()
    appName: str
    version: str
    environment: str

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance.app_name = "Eduvos Enterprise Application"
                    instance.version = "1.0"
                    instance.environment = "Development"
                    cls._instance = instance
        return cls._instance

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def displayConfig(self) -> None:
        print(f"Application Name: {self.app_name}")
        print(f"Version: {self.version}")
        print(f"Environment: {self.environment}")
