class TechnicalTicket:
    def __init__(self, ticketID, learner, issue):
        self.ticketID = ticketID
        self.learner = learner
        self.issue = issue
        self.type = "Technical"

    def displayInfo(self):
        print("Ticket ID:", self.ticketID)
        print("Type:", self.type)
        print("Learner:", self.learner.name)
        print("Issue:", self.issue)


class RegistrationTicket:
    def __init__(self, ticketID, learner, issue):
        self.ticketID = ticketID
        self.learner = learner
        self.issue = issue
        self.type = "Registration"

    def displayInfo(self):
        print("Ticket ID:", self.ticketID)
        print("Type:", self.type)
        print("Learner:", self.learner.name)
        print("Issue:", self.issue)


class AssessmentTicket:
    def __init__(self, ticketID, learner, issue):
        self.ticketID = ticketID
        self.learner = learner
        self.issue = issue
        self.type = "Assessment"

    def displayInfo(self):
        print("Ticket ID:", self.ticketID)
        print("Type:", self.type)
        print("Learner:", self.learner.name)
        print("Issue:", self.issue)


class SupportTicketFactory:

    @staticmethod
    def createTicket(ticketType, ticketID, learner, issue):

        if ticketType == "technical":
            return TechnicalTicket(ticketID, learner, issue)

        elif ticketType == "registration":
            return RegistrationTicket(ticketID, learner, issue)

        elif ticketType == "assessment":
            return AssessmentTicket(ticketID, learner, issue)

        else:
            raise ValueError("Invalid support ticket type.")