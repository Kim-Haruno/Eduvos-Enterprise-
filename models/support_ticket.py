from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.learner import Learner


class SupportTicket:

    def __init__(self, ticketID: str, learner: Learner, issue: str) -> None:
        if not isinstance(ticketID, str) or not ticketID.strip():
            raise ValueError("Ticket ID cannot be empty.")
        from models.learner import Learner as LearnerType

        if not isinstance(learner, LearnerType):
            raise TypeError("learner must be a Learner instance.")
        if not isinstance(issue, str) or not issue.strip():
            raise ValueError("Support issue cannot be empty.")
        self.ticketID = ticketID.strip()
        self.learner = learner
        self.issue = issue.strip()
        self.status = "Open"
        self.createdDate = datetime.now()

    @property
    def ID(self) -> str:
        return self.ticketID

    def closeTicket(self) -> None:
        self.status = "Closed"

    def __str__(self) -> str:
        return f"{self.ticketID} - {self.status}: {self.issue}"

    def __repr__(self) -> str:
        return f"SupportTicket({self.ticketID!r}, {self.learner!r}, {self.issue!r})"

    def displayInfo(self) -> None:
        print(f"Ticket ID: {self.ticketID}")
        print(f"Learner: {self.learner.name}")
        print(f"Issue: {self.issue}")
        print(f"Status: {self.status}")
        print(f"Created: {self.createdDate.isoformat(sep=' ', timespec='seconds')}")
