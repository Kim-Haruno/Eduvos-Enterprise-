class Course:
    def __init__(self, courseID, courseName, capacity):
        self.validateCourse(courseID, courseName, capacity)

        self.courseID = courseID
        self.courseName = courseName
        self.capacity = capacity
        self.registeredLearners = []

    def validateCourse(self, courseID, courseName, capacity):
        if not courseID:
            raise ValueError("Course ID cannot be empty.")

        if not courseName:
            raise ValueError("Course name cannot be empty.")

        if capacity <= 0:
            raise ValueError("Course capacity must be greater than zero.")

    def addLearner(self, learner):
        if len(self.registeredLearners) >= self.capacity:
            print("Course is full.")
            return False

        self.registeredLearners.append(learner)
        print(f"{learner.name} successfully registered for {self.courseName}.")
        return True

    def displayInfo(self):
        print("Course ID:", self.courseID)
        print("Course Name:", self.courseName)
        print("Capacity:", self.capacity)
        print("Registered Learners:", len(self.registeredLearners))