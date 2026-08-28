class SupportTicket:
    def __init__(self, ticketID, learner, issue):
        self.validateTicket(ticketID, issue)

        self.ticketID = ticketID
        self.learner = learner
        self.issue = issue
        self.status = "Open"

    def validateTicket(self, ticketID, issue):
        if not ticketID:
            raise ValueError("Ticket ID cannot be empty.")

        if not issue:
            raise ValueError("Support issue cannot be empty.")

    def closeTicket(self):
        self.status = "Closed"

    def displayInfo(self):
        print("Ticket ID:", self.ticketID)
        print("Learner:", self.learner.name)
        print("Issue:", self.issue)
        print("Status:", self.status)