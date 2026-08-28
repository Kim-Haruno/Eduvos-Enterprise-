class Registration:
    def __init__(self, registrationID, learner, course):
        self.registrationID = registrationID
        self.learner = learner
        self.course = course
        self.status = "Pending"

    def approve(self):
        self.status = "Approved"

    def reject(self):
        self.status = "Rejected"

    def displayInfo(self):
        print("Registration ID:", self.registrationID)
        print("Learner:", self.learner.name)
        print("Course:", self.course.courseName)
        print("Status:", self.status)