from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from models.course import Course
    from models.learner import Learner

RegistrationStatus = Literal["Pending", "Approved", "Rejected"]


class Registration:

    def __init__(
        self,
        registrationID: str,
        learner: Learner,
        course: Course,
        status: RegistrationStatus = "Pending",
    ) -> None:
        if not isinstance(registrationID, str) or not registrationID.strip():
            raise ValueError("Registration ID cannot be empty.")
        from models.course import Course as CourseType
        from models.learner import Learner as LearnerType

        if not isinstance(learner, LearnerType):
            raise TypeError("learner must be a Learner instance.")
        if not isinstance(course, CourseType):
            raise TypeError("course must be a Course instance.")
        if status not in {"Pending", "Approved", "Rejected"}:
            raise ValueError("Registration status must be Pending, Approved, or Rejected.")
        self.registrationID = registrationID.strip()
        self.learner = learner
        self.course = course
        self.status: RegistrationStatus = status
        learner.registrations.append(self)
        course.registrations.append(self)

    @property
    def ID(self) -> str:
        return self.registrationID

    def approve(self) -> None:
        self.status = "Approved"

    def reject(self) -> None:
        self.status = "Rejected"

    def __str__(self) -> str:
        return f"{self.registrationID} - {self.learner.name} - {self.course.courseName} ({self.status})"

    def __repr__(self) -> str:
        return f"Registration({self.registrationID!r}, {self.learner!r}, {self.course!r})"

    def displayInfo(self) -> None:
        print(f"Registration ID: {self.registrationID}")
        print(f"Learner: {self.learner.name}")
        print(f"Course: {self.course.courseName}")
        print(f"Status: {self.status}")
