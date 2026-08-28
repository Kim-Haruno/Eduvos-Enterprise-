class Learner:
    def __init__(self, learnerID, name, email):
        self.validateLearner(learnerID, name, email)

        self.learnerID = learnerID
        self.name = name
        self.email = email

    def validateLearner(self, learnerID, name, email):
        if not learnerID:
            raise ValueError("Learner ID cannot be empty.")

        if not name:
            raise ValueError("Learner name cannot be empty.")

        if "@" not in email:
            raise ValueError("Invalid email address.")

    def displayInfo(self):
        print("Learner ID:", self.learnerID)
        print("Name:", self.name)
        print("Email:", self.email)