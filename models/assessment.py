class Assessment:
    def __init__(self, assessmentID, learner, course, mark):
        self.validateAssessment(assessmentID, mark)

        self.assessmentID = assessmentID
        self.learner = learner
        self.course = course
        self.mark = mark
        self.result = self.calculateResult()

    def validateAssessment(self, assessmentID, mark):
        if not assessmentID:
            raise ValueError("Assessment ID cannot be empty.")

        if mark < 0 or mark > 100:
            raise ValueError("Assessment mark can only be between 0 and 100.")

    def calculateResult(self):
        if self.mark >= 50:
            return "Pass"
        else:
            return "Fail"

    def displayInfo(self):
        print("Assessment ID:", self.assessmentID)
        print("Learner:", self.learner.name)
        print("Course:", self.course.courseName)
        print("Mark:", self.mark)
        print("Result:", self.result)