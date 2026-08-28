from typing import TYPE_CHECKING

from models.learner import Learner

if TYPE_CHECKING:
    from models.learner import Learner
    from models.registration import Registration


class Course:
    def __init__(self, courseID: str, courseName: str, capacity: int) -> None:
        if not isinstance(courseID, str) or not courseID.strip():
            raise ValueError("Course ID cannot be empty.")
        if not isinstance(courseName, str) or not courseName.strip():
            raise ValueError("Course name cannot be empty.")
        if (
            not isinstance(capacity, int)
            or isinstance(capacity, bool)
            or capacity <= 0
        ):
            raise ValueError("Course capacity must be a positive integer.")
        self.courseID = courseID.strip()
        self.courseName = courseName.strip()
        self.capacity = capacity
        self.registeredLearners: list[Learner] = []
        self.registrations: list[Registration] = []

    @property
    def ID(self) -> str:
        return self.courseID

    @property
    def name(self) -> str:
        return self.courseName

    def addLearner(self, learner: Learner) -> bool:
        if not isinstance(learner, Learner):
            raise TypeError("learner must be a Learner instance.")
        if learner in self.registeredLearners:
            return False
        if len(self.registeredLearners) >= self.capacity:
            return False
        self.registeredLearners.append(learner)
        return True

    def __str__(self) -> str:
        return f"{self.courseID} - {self.courseName} ({len(self.registeredLearners)}/{self.capacity})"

    def __repr__(self) -> str:
        return f"Course({self.courseID!r}, {self.courseName!r}, {self.capacity!r})"

    def displayInfo(self) -> None:
        print(f"Course ID: {self.courseID}")
        print(f"Course Name: {self.courseName}")
        print(f"Capacity: {self.capacity}")
        print(f"Registered Learners: {len(self.registeredLearners)}")
