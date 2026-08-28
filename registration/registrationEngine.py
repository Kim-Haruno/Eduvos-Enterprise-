from concurrent.futures import ThreadPoolExecutor
import threading
from typing import Any, Iterable

from models.registration import Registration
from monitoring.bugzot import Bugzot


class RegistrationEngine:

    def __init__(self, maxWorkers: int = 5) -> None:
        if not isinstance(maxWorkers, int) or isinstance(maxWorkers, bool) or maxWorkers <= 0:
            raise ValueError("max_workers must be greater than zero.")
        self.registrations: list[Registration] = []
        self.lock = threading.Lock()
        self.maxWorkers = maxWorkers

    @staticmethod
    def validateRegistration(registration: Registration) -> None:
        if not isinstance(registration, Registration):
            raise TypeError("registration must be a Registration instance.")
        if registration.learner is None or registration.course is None:
            raise ValueError("Registration must have a learner and course.")

    def processRegistration(self, registration: Registration) -> str:
        startTime = Bugzot.startTimer()
        try:
            self.validateRegistration(registration)
        except (TypeError, ValueError) as error:
            Bugzot.logEvent(
                "VALIDATION",
                "Registration validation failed",
                str(error),
                level="ERROR",
            )
            Bugzot.recordPerformance("Registration validation", startTime)
            raise

        if registration.status != "Pending":
            Bugzot.recordPerformance("Finalized registration check", startTime)
            return f"Skipped: Registration already {registration.status}"

        learner = registration.learner
        course = registration.course

        with self.lock:
            for existing in self.registrations:
                if (
                    existing.learner.learnerID == learner.learnerID
                    and existing.course.courseID == course.courseID
                ):
                    registration.reject()
                    Bugzot.logEvent(
                        "DUPLICATE",
                        "Duplicate registration attempt",
                        f"Learner: {learner.name}, Course: {course.courseName}",
                        level="WARNING",
                    )
                    Bugzot.recordPerformance("Duplicate registration check", startTime)
                    return "Rejected: Duplicate registration"

            if not course.addLearner(learner):
                registration.reject()
                Bugzot.logEvent(
                    "CAPACITY",
                    "Course capacity exceeded",
                    f"Course: {course.courseName}, Capacity: {course.capacity}",
                    level="WARNING",
                )
                Bugzot.recordPerformance("Course capacity check", startTime)
                return "Rejected: Course is full"

            registration.approve()
            self.registrations.append(registration)
            Bugzot.logEvent(
                "REGISTRATION",
                "Registration approved",
                f"Learner: {learner.name}, Course: {course.courseName}",
                level="INFO",
            )
            Bugzot.recordPerformance("Registration processing", startTime)
            return "Approved: Registration successful"

    def result(self, registration: Registration, result: str) -> dict[str, Any]:
        return {
            "registrationID": registration.registrationID,
            "learner": registration.learner.name,
            "course": registration.course.courseName,
            "status": registration.status,
            "result": result,
        }

    def processRequests(self, requests: Iterable[Registration]) -> list[dict[str, Any]]:
        return [
            self.result(registration, self.processRegistration(registration))
            for registration in requests
        ]

    def processRequestsConcurrently(
        self, requests: Iterable[Registration]
    ) -> list[dict[str, Any]]:
        request_list = list(requests)
        with ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
            futures = [
                executor.submit(self.processRegistration, registration)
                for registration in request_list
            ]
            return [
                self.result(registration, future.result())
                for registration, future in zip(request_list, futures)
            ]

    def displaySummary(self, results: list[dict[str, Any]]) -> None:
        successful = sum(result["status"] == "Approved" for result in results)
        print("\n===== REGISTRATION PROCESSING SUMMARY =====")
        for result in results:
            print(
                f"{result['registrationID']} | {result['learner']} | "
                f"{result['course']} | {result['status']} | {result['result']}"
            )
        print(f"\nTotal Requests: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Rejected: {len(results) - successful}")

