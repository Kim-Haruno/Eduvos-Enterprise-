from concurrent.futures import ThreadPoolExecutor
from monitoring.bugzot import Bugzot
import threading
import time


class RegistrationEngine:

    def __init__(self):
        self.registrations = []
        self.lock = threading.Lock()


    def processRegistration(self, registration):

        start_time = Bugzot.startTimer()

        learner = registration.learner
        course = registration.course


        with self.lock:
            for existing in self.registrations:
                if (existing.learner.learnerID == learner.learnerID and
                        existing.course.courseID == course.courseID):
                    registration.reject()
                    Bugzot.logEvent(
                        "DUPLICATE",
                        "Duplicate registration attempt",
                        f"Learner: {learner.name}, Course: {course.courseName}"
                    )
                    Bugzot.recordPerformance(
                        "Duplicate registration check",
                        start_time
                    )
                    return "Rejected: Duplicate registration"

            if len(course.registeredLearners) >= course.capacity:
                registration.reject()
                Bugzot.logEvent(
                    "CAPACITY",
                    "Course capacity exceeded",
                    f"Course: {course.courseName}, Capacity: {course.capacity}"
                )
                Bugzot.recordPerformance(
                    "Course capacity check",
                    start_time
                )


                return "Rejected: Course is full"

            course.addLearner(learner)
            registration.approve()
            self.registrations.append(registration)
            Bugzot.logEvent(
                "REGISTRATION",
                "Registration approved",
                f"Learner: {learner.name}, Course: {course.courseName}"
            )
            Bugzot.recordPerformance(
                "Registration processing",
                start_time
            )

            return "Approved: Registration successful"

    def processRequests(self, requests):
        results = []

        for registration in requests:
            result = self.processRegistration(registration)
            results.append({
                "registration_id": registration.registrationID,
                "learner": registration.learner.name,
                "course": registration.course.courseName,
                "status": registration.status,
                "result": result
            })

        return results

    def processRequestsConcurrently(self, requests):
        results = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.processRegistration, registration)
                for registration in requests
            ]

            for registration, future in zip(requests, futures):
                result = future.result()
                results.append({
                    "registrationID": registration.registrationID,
                    "learner": registration.learner.name,
                    "course": registration.course.courseName,
                    "status": registration.status,
                    "result": result
                })

        return results

    def displaySummary(self, results):
        successful = 0
        rejected = 0

        print("\n===== REGISTRATION PROCESSING SUMMARY =====")

        for result in results:
            registration_id = result.get("registration_id", result.get("registrationID"))
            print(
                f"{registration_id} | "
                f"{result['learner']} | "
                f"{result['course']} | "
                f"{result['status']} | "
                f"{result['result']}"
            )

            if result["status"] == "Approved":
                successful += 1
            else:
                rejected += 1

        print("\nTotal Requests:", len(results))
        print("Successful:", successful)
        print("Rejected:", rejected)