from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.course import Course
    from models.learner import Learner


class Assessment:

    def __init__(
        self,
        assessmentID: str,
        learner: Learner,
        course: Course,
        score: float,
        assessmentDate: date | None = None,
    ) -> None:
        if not isinstance(assessmentID, str) or not assessmentID.strip():
            raise ValueError("Assessment ID cannot be empty.")
        from models.course import Course as CourseType
        from models.learner import Learner as LearnerType

        if not isinstance(learner, LearnerType):
            raise TypeError("learner must be a Learner instance.")
        if not isinstance(course, CourseType):
            raise TypeError("course must be a Course instance.")
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 100:
            raise ValueError("Assessment score must be between 0 and 100.")
        if assessmentDate is not None and not isinstance(assessmentDate, date):
            raise ValueError("Assessment date must be a date.")
        self.assessmentID = assessmentID.strip()
        self.learner = learner
        self.course = course
        self.score = score
        self.date = assessmentDate or date.today()
        self.result = self.calculateResult()

    @property
    def ID(self) -> str:
        return self.assessmentID

    def calculateResult(self) -> str:
        return "Pass" if self.score >= 50 else "Fail"

    def __str__(self) -> str:
        return f"{self.assessmentID} - {self.learner.name}: {self.score}/100 ({self.result})"

    def __repr__(self) -> str:
        return f"Assessment({self.assessmentID!r}, {self.learner!r}, {self.course!r}, {self.score!r})"

    def displayInfo(self) -> None:
        print(f"Assessment ID: {self.assessmentID}")
        print(f"Learner: {self.learner.name}")
        print(f"Course: {self.course.courseName}")
        print(f"Score: {self.score}")
        print(f"Date: {self.date.isoformat()}")
        print(f"Result: {self.result}")
