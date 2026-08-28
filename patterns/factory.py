from models.learner import Learner
from models.support_ticket import SupportTicket


class AcademicTicket(SupportTicket):

    ticket_type = "Academic"


class TechnicalTicket(SupportTicket):

    ticket_type = "Technical"


class RegistrationTicket(SupportTicket):

    ticket_type = "Registration"


class SupportTicketFactory:

    ticketTypes: dict[str, type[SupportTicket]] = {
        "academic": AcademicTicket,
        "assessment": AcademicTicket,
        "technical": TechnicalTicket,
        "registration": RegistrationTicket,
    }

    @staticmethod
    def createTicket(
        ticketType: str, ticketID: str, learner: Learner, issue: str
    ) -> SupportTicket:
        if not isinstance(ticketType, str) or not ticketType.strip():
            raise ValueError("Support ticket type cannot be empty.")
        ticketClass = SupportTicketFactory.ticketTypes.get(ticketType.strip().lower())
        if ticketClass is None:
            raise ValueError("Invalid support ticket type.")
        return ticketClass(ticketID, learner, issue)
