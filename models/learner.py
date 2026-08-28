import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.registration import Registration


class Learner:

    def __init__(self, learnerID: str, name: str, email: str) -> None:
        self.validate(learnerID, name, email)
        self.learnerID = learnerID.strip()
        self.name = name.strip()
        self.email = email.strip()
        self.registrations: list[Registration] = []

    @property
    def ID(self) -> str:
        return self.learnerID

    @staticmethod
    def validate(learnerID: str, name: str, email: str) -> None:
        if not isinstance(learnerID, str) or not learnerID.strip():
            raise ValueError("Learner ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Learner name cannot be empty.")
        if not isinstance(email, str) or not re.fullmatch(
            r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip()
        ):
            raise ValueError("Invalid email address.")

    def __str__(self) -> str:
        return f"{self.learnerID} - {self.name} ({self.email})"

    def __repr__(self) -> str:
        return f"Learner({self.learnerID!r}, {self.name!r}, {self.email!r})"

    def displayInfo(self) -> None:
        print(f"Learner ID: {self.learnerID}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
